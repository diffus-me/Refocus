from collections.abc import Callable

from modules.settings import default_settings

import os
import cv2
import imageio
import numpy as np
import rembg
import torch
import PIL.Image
from PIL import Image
from typing import Any


class pipeline:
    def remove_background(
        self,
        image: PIL.Image.Image,
        rembg_session: Any = None,
        force: bool = False,
        **rembg_kwargs,
    ) -> PIL.Image.Image:
        do_remove = True
        if image.mode == "RGBA" and image.getextrema()[3][0] < 255:
            do_remove = False
        do_remove = do_remove or force
        if do_remove:
            image = rembg.remove(image, session=rembg_session, **rembg_kwargs)
        return image

    pipeline_type = ["rembg"]
    model_hash = ""

    # Optional function
    def parse_gen_data(self, gen_data):
        return gen_data

    def load_base_model(self, name):
        return

    def load_keywords(self, lora):
        return " "

    def load_loras(self, loras):
        return

    def refresh_controlnet(self, name=None):
        return

    def clean_prompt_cond_caches(self):
        return

    def process(
        self,
        positive_prompt,
        negative_prompt,
        input_image,
        controlnet,
        main_view,
        steps,
        width,
        height,
        image_seed,
        start_step,
        denoise,
        cfg,
        sampler_name,
        scheduler,
        clip_skip,
        callback,
        gen_data=None,
        progressbar: Callable | None = None,
    ):

        if progressbar:
            progressbar(1, "Removing background ...")

        rembg_session = rembg.new_session()
        input_image = self.remove_background(input_image, rembg_session)

        # Return finished image to preview
        if callback is not None:
            callback(steps, 0, 0, steps, input_image)

        return [input_image]
