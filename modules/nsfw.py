#!/usr/bin/env python3

import time
from typing import TYPE_CHECKING

import numpy as np
import opennsfw2 as n2
from keras import Model
from PIL import Image, ImageFilter

if TYPE_CHECKING:
    from modules.async_worker import AsyncTask

_OPEN_NSFW_MODEL: Model | None = None


def _get_open_nsfw_model() -> Model:
    global _OPEN_NSFW_MODEL

    if _OPEN_NSFW_MODEL is None:
        _OPEN_NSFW_MODEL = n2.make_open_nsfw_model()

    return _OPEN_NSFW_MODEL


def _get_nsfw_probability(image: Image.Image) -> float:
    preprocess_image = n2.preprocess_image(image, n2.Preprocessing.YAHOO)
    inputs = np.expand_dims(preprocess_image, axis=0)

    model = _get_open_nsfw_model()
    predictions = model.predict(inputs)
    _, nsfw_probability = predictions[0]

    return nsfw_probability


def nsfw_blur(image: Image.Image, async_task: "AsyncTask", threshold=0.75) -> Image.Image | None:
    if async_task.metadata is None or async_task.metadata["user-tier"].lower() != "free":
        return None

    print("[NSFW] Start detecting NSFW content")

    start_at = time.perf_counter()
    probability = _get_nsfw_probability(image)
    ended_at = time.perf_counter()
    print(f"[NSFW] NSFW probability is {probability}, threshold is {threshold}")
    print(f"[NSFW] Detecting NSFW has taken: {(ended_at - start_at):.2f} seconds")

    if probability > threshold:
        return image.filter(ImageFilter.BoxBlur(10))

    return None
