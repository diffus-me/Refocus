from collections.abc import Callable

from modules.settings import default_settings

from PIL import Image

# Copy this file, add suitable code and add logic to modules/pipelines.py to select it


class pipeline:
    pipeline_type = ["template"]

    model_hash = ""

    # Optional function
    def parse_gen_data(self, gen_data):
        gen_data["ruinedfooocus_was_here"] = True
        return gen_data

    def load_base_model(self, name):
        # Check if model is already loaded
        if self.model_hash == name:
            return
        print(f"Loading model: {name}")
        self.model_hash = name
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

        images = Image.open("logo.png")

        # Return finished image to preview
        if callback is not None:
            callback(steps, 0, 0, steps, images)

        return [images]
