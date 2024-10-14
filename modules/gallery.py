#!/usr/bin/env python3

import json
import logging
import random
import time
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

import redis
import requests

from settings import settings

if TYPE_CHECKING:
    from modules.async_worker import AsyncTask

_feature_permissions = None

logger = logging.getLogger("default")


class RedisClient:
    def __init__(self, url: str) -> None:
        self._url = url
        self._client: redis.Redis | None = None

    def reset(self) -> None:
        self._client = None

    def new_client(self) -> redis.Redis:
        client = redis.Redis.from_url(self._url)
        client.ping()

        return client

    def scan_iter(
        self, pattern: str, count: int | None = None, _type: str | None = None
    ) -> Iterator[str]:
        if self._client is None:
            self._client = self.new_client()

        return self._client.scan_iter(pattern, count, _type)

    def get(self, name: str) -> str | bytes | None:
        if self._client is None:
            self._client = self.new_client()

        return self._client.get(name)


_redis_client = RedisClient(settings.redis_address)


def _find_gallery_endpoint(retry: int = 3) -> str:
    endpoints = []
    for i in range(retry):
        if i != 0:
            logger.info(f"No up ports from redis, retring i({i})")
            time.sleep(i * 5)

        for instance_id in _redis_client.scan_iter("service:gallery_*"):
            response = _redis_client.get(instance_id)
            if not isinstance(response, (str, bytes)):
                logger.error(
                    "Get invalid response from redis: "
                    f"response({response}), instance_id({instance_id})"
                )
                continue

            node_status = json.loads(response)

            if node_status["status"].lower() == "up":
                endpoints.append(
                    f"{node_status['schema']}://{node_status['ip']}:{node_status['port']}"
                )

        if endpoints:
            return random.choice(endpoints)

    raise ValueError("No up ports from redis")


def get_feature_permissions(session: requests.Session) -> dict[str, Any]:
    global _feature_permissions

    if _feature_permissions is None:
        url = settings.feature_permissions_url
        if not url:
            message = f"Failed to get feature permissions url from env"
            raise ValueError(message)

        response = session.get(url)
        response.raise_for_status()
        content = response.json()

        _feature_permissions = {
            "generate": {item["name"]: item for item in content["generate"]},
            "buttons": {item["name"]: item for item in content["buttons"]},
            "features": {item["name"]: item for item in content["features"]},
        }

    return _feature_permissions


def register(task: "AsyncTask", pnginfo: dict[str, Any], path: Path) -> None:
    assert task.task_type
    assert task.metadata

    url = f"{_find_gallery_endpoint()}/gallery-api/v1/images"

    session = requests.Session()
    permissions = get_feature_permissions(session)
    is_public = (
        task.metadata["user-tier"] not in permissions["features"]["PrivateImage"]["allowed_tiers"]
    )

    geninfo = pnginfo["parameters"]

    if geninfo.get("Upscale Mode") == "Fast":
        prompt = None
        base = None
    else:
        prompt = geninfo["Prompt"]
        base = task.task_type.upper()

    body = {
        "task_id": task.task_id,
        "path": str(path.relative_to(settings.workdir_jfs_target)),
        "feature": "REFOCUS",
        "base": base,
        "prompt": prompt,
        "pnginfo": json.dumps(pnginfo),
        "created_by": task.metadata["user-id"],
        "model_ids": [],
        "is_public": is_public,
    }

    response = session.post(url, json=body)
    print(response.text)
    response.raise_for_status()
