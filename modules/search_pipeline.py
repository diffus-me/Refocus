from collections.abc import Callable

from modules.settings import default_settings
import shared
import glob
from pathlib import Path
import datetime
import re
import json

from PIL import Image

# Copy this file, add suitable code and add logic to modules/pipelines.py to select it

def search_for_words(searchfor, prompt):
    searchfor = searchfor.lower()
    prompt = prompt.lower()
    words = searchfor.split(",")
    result = True
    for word in words:
        word = word.strip()
        if word not in prompt:
            result = False
            break
    return result


class pipeline:
    pipeline_type = ["search"]

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
        if progressbar:
            progressbar(1, "Searching ...")
        images = []
        maxresults = gen_data["original_image_number"]
        maxresults = 100 if maxresults <= 1 else maxresults # 0 and 1 is 100 matches (max)
        skip = 0

        folder=shared.path_manager.model_paths["temp_outputs_path"]
        current_time = datetime.datetime.now()
        daystr = current_time.strftime("%Y-%m-%d")

        # Parse search arguments
        searchfor = re.sub(r"search: *", "", positive_prompt, count=1)

        chomp = True # Do this until we can't chomp off any more options
        while chomp:
            chomp = False

            # Date
            matchstr = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\s?"
            match = re.match(matchstr, searchfor)
            if match is not None:
                daystr = match.group().strip()
                searchfor = re.sub(matchstr, "", searchfor)
                chomp = True

            # Skip
            matchstr = r"^skip:\s?(?P<skip>[0-9]+)\s?"
            match = re.match(matchstr, searchfor)
            if match is not None:
                skip = int(match.group("skip"))
                searchfor = re.sub(matchstr, "", searchfor)
                chomp = True

            # Skip more
            matchstr = r"^\+(?P<skip>[0-9]+)\s?"
            match = re.match(matchstr, searchfor)
            if match is not None:
                skip += int(match.group("skip"))
                searchfor = re.sub(matchstr, "", searchfor)
                chomp = True

            # Set max
            matchstr = r"^max:\s?(?P<max>[0-9]+)\s?"
            match = re.match(matchstr, searchfor)
            if match is not None:
                maxresults = int(match.group("max"))
                searchfor = re.sub(matchstr, "", searchfor)
                chomp = True

        searchfor = searchfor.strip()

        # For all folder/daystr/*.png ... match metadata
        pngs = glob.glob(str(Path(folder) / daystr / "*.*"))

        found = 0
        for file in pngs:
            im = Image.open(file)
            metadata = {"prompt": ""}
            if im.info.get("parameters"):
                metadata = json.loads(im.info["parameters"])

            # Show image if metadata is missing. (like for gifs)
            if searchfor == "" or "Prompt" not in metadata or search_for_words(searchfor, metadata["Prompt"]):
                # Return finished image to preview
                if callback is not None and found > skip:
                    callback(found - skip, 0, 0, maxresults, None) # Returning im here is a bit much...
                images.append(file)
                found += 1
            if found >= (maxresults + skip):
                break

        return images[skip:]
