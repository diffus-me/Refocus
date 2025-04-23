#!/usr/bin/env python3

import time
from typing import TYPE_CHECKING, Any

import numpy as np
import requests
from PIL import Image, ImageFilter

from api import numpy_array_to_base64
from settings import settings

if TYPE_CHECKING:
    from modules.async_worker import AsyncTask

_feature_permissions = None


def get_feature_permissions() -> dict[str, Any]:
    global _feature_permissions

    if _feature_permissions is None:
        url = settings.feature_permissions_url
        if not url:
            message = "Failed to get feature permissions url from env"
            raise ValueError(message)

        response = requests.get(url)
        response.raise_for_status()
        content = response.json()

        _feature_permissions = {
            "generate": {item["name"]: item for item in content["generate"]},
            "buttons": {item["name"]: item for item in content["buttons"]},
            "features": {item["name"]: item for item in content["features"]},
        }

    return _feature_permissions


def _check_nsfw(endpoint: str, image: np.array, prompt: str) -> dict[str, Any]:
    url = f"{endpoint}/api/v3/internal/moderation/content"
    body = {
        "text": prompt,
        "image": {"encoded_image": numpy_array_to_base64(image)},
    }

    response = requests.post(url, json=body)
    response.raise_for_status()

    result = response.json()

    return result


def nsfw_blur(
    image: np.array, prompt: str, async_task: "AsyncTask"
) -> tuple[Image.Image | None, dict[str, Any] | None]:
    assert async_task.metadata is not None

    allowed_tiers = get_feature_permissions()["features"]["NSFWContent"]["allowed_tiers"]
    if async_task.metadata["user-tier"] in allowed_tiers:
        return None, None

    endpoint = async_task.metadata["x-diffus-api-gateway-endpoint"]

    print("[NSFW] Start detecting NSFW content")

    start_at = time.perf_counter()
    result = _check_nsfw(endpoint, image, prompt)
    ended_at = time.perf_counter()

    print(f"[NSFW] Detecting NSFW has taken: {(ended_at - start_at):.2f} seconds")

    if result["flag"]:
        return Image.fromarray(image).filter(ImageFilter.BoxBlur(10)), result

    return None, result
