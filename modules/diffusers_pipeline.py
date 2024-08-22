from collections.abc import Callable

from modules.settings import default_settings
import torch
import diffusers
import re
import os
from pathlib import Path

from PIL import Image
from shared import path_manager
import json

class pipeline:
    pipeline_type = ["diffusers"]

    model_hash = ""
    model_class = ""
    pipe = None

#    def parse_gen_data(self, gen_data):
#        return gen_data

    def load_base_model(self, name):
        # Check if model is already loaded
        if self.model_hash == name:
            return
        print(f"Loading model: {name}")
        self.model_hash = name
        repo_id = re.sub(r"🤗:", "", name, count=1)
        folder = os.path.join(path_manager.model_paths["diffusers_path"], repo_id)

        model_index = os.path.join(folder, "model_index.json")

        if Path(model_index).exists():
            try:
                with open(model_index) as f:
                    model_json = json.load(f)
            except:
                model_json = None

        self.model_class = model_json["_class_name"]

        diffusers_pipeline = None
        if self.model_class == "PixArtSigmaPipeline":
            diffusers_pipeline = diffusers.PixArtSigmaPipeline
        elif self.model_class == "FluxPipeline":
            diffusers_pipeline = diffusers.FluxPipeline
        elif self.model_class == "WuerstchenDecoderPipeline":
            diffusers_pipeline = diffusers.AutoPipelineForText2Image
        elif self.model_class == "StableDiffusionPipeline":
            diffusers_pipeline = diffusers.StableDiffusionPipeline
        elif self.model_class == "StableDiffusionXLPipeline":
            diffusers_pipeline = diffusers.StableDiffusionXLPipeline

        if diffusers_pipeline == None:
            print(f"ERRROR: Unknown diffuser pipeline: {model_json['_class_name']}")
            self.pipe = None
            return

        self.pipe = diffusers_pipeline.from_pretrained(
            folder,
            local_files_only = False,
            cache_dir = path_manager.model_paths["diffusers_cache_path"],
            torch_dtype=torch.bfloat16
            )
        self.pipe.enable_sequential_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power
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
        if progressbar:
            progressbar(1, "Generating ...")

        seed = image_seed

        image = self.pipe(
            prompt=positive_prompt,
            height=height,
            width=width,
            guidance_scale=cfg,
            output_type="pil",
            num_inference_steps=steps,
            max_sequence_length=256,
            generator=torch.Generator("cpu").manual_seed(seed)
        ).images[0]

        # Return finished image to preview
        if callback is not None:
            callback(steps, 0, 0, steps, image)

        return [image]
