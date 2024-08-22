from collections.abc import Callable

from modules.settings import default_settings
import shared
import glob
from pathlib import Path
import datetime
import re
import json
from huggingface_hub import snapshot_download

from PIL import Image


class pipeline:
    pipeline_type = ["hugginface_dl"]

    model_hash = ""

    def parse_gen_data(self, gen_data):
        gen_data["original_image_number"] = gen_data["image_number"]
        gen_data["image_number"] = 1
        gen_data["show_preview"] = False
        return gen_data

    def load_base_model(self, name):
        # We're not doing models here
        return

    def load_keywords(self, lora):
        filename = lora.replace(".safetensors", ".txt")
        try:
            with open(filename, "r") as file:
                data = file.read()
            return data
        except FileNotFoundError:
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
        print(f"Downloading: {positive_prompt}")

        repo_id = re.sub(r"^\s*hf:\s*", "", positive_prompt, count=1)
        repo_id = re.sub(r"\s.*$", "", repo_id, count=1)
        repo_id = repo_id.replace(",", "")

        if progressbar:
            progressbar(1, f"Downloading {repo_id}...")

        snapshot_download(
            repo_id=repo_id,
            local_dir=f"models/diffusers/{repo_id}",
            resume_download=True,
        )

        images = ["logo.png"]

        return images
