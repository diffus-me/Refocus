import torch
import os
import einops
from latent_preview import Latent2RGBPreviewer
import numpy as np


def clean_prompt_cond_caches():
    conditions = {}
    conditions["+"] = {}
    conditions["-"] = {}
    conditions["switch"] = {}
    conditions["+"]["text"] = None
    conditions["+"]["cache"] = None
    conditions["-"]["text"] = None
    conditions["-"]["cache"] = None
    conditions["switch"]["text"] = None
    conditions["switch"]["cache"] = None
    return conditions


def set_timestep_range(conditioning, start, end):
    c = []
    for t in conditioning:
        if "pooled_output" in t:
            t["start_percent"] = start
            t["end_percent"] = end

    return conditioning

def get_previewer(device, latent_format):
    previewer = Latent2RGBPreviewer(latent_format.latent_rgb_factors)
    def preview_function(x0, step, total_steps):
        return previewer.decode_latent_to_preview(x0)
    previewer.preview = preview_function
    return previewer
