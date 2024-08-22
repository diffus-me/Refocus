import os
import shutil
import json
from os.path import exists
from shared import state

DEFAULT_CNSETTINGS_FILE = "settings/powerup.default"
CNSETTINGS_FILE = "settings/powerup.json"
NEWCN = "Custom..."

# https://huggingface.co/stabilityai/control-lora/tree/main/control-LoRAs-rank128
controlnet_models = {
    "canny": "control-lora-canny-rank128.safetensors",
    "depth": "control-lora-depth-rank128.safetensors",
    "recolour": "control-lora-recolor-rank128.safetensors",
    "sketch": "control-lora-sketch-rank128-metadata.safetensors",
    "img2img": None,
    "upscale": None,
    "layerdiffusion": None,
    # "faceswap": None,
}

import json
import os
import shutil


def load_cnsettings():
    settings = {}
    if not os.path.isfile(CNSETTINGS_FILE):
        shutil.copy(DEFAULT_CNSETTINGS_FILE, CNSETTINGS_FILE)

    if os.path.exists(CNSETTINGS_FILE):
        with open(CNSETTINGS_FILE) as f:
            settings.update(json.load(f))

    with open(DEFAULT_CNSETTINGS_FILE) as f:
        default_settings = json.load(f)

    # Update settings with any missing keys from default_settings
    settings_updated = False
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
            settings_updated = True

    # If settings were updated, write them back to the file
    if settings_updated:
        with open(CNSETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)

    return settings


def save_cnsettings(cn_save_options):
    global controlnet_settings, cn_options
    with open(CNSETTINGS_FILE, "w") as f:
        json.dump(cn_save_options, f, indent=2)
    controlnet_settings = cn_save_options
    cn_options = {f"{k}": v for k, v in controlnet_settings.items()}


def modes():
    return controlnet_settings.keys()


def get_model(type):
    return controlnet_models[type] if type in controlnet_models else None


def get_settings(gen_data):
    if "cn_selection" not in gen_data:
        return {}
    if gen_data["cn_selection"] == NEWCN:
        return {
            "type": gen_data["cn_type"].lower(),
            "edge_low": gen_data["cn_edge_low"],
            "edge_high": gen_data["cn_edge_high"],
            "start": gen_data["cn_start"],
            "stop": gen_data["cn_stop"],
            "strength": gen_data["cn_strength"],
            "upscaler": gen_data["cn_upscale"],
        }
    else:
        return (
            controlnet_settings[gen_data["cn_selection"]]
            if gen_data["cn_selection"] in controlnet_settings
            else {}
        )


controlnet_settings = load_cnsettings()
cn_options = {f"{k}": v for k, v in controlnet_settings.items()}
