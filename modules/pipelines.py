import gc 
import logging
from shared import state, path_manager
from modules.civit import Civit
from pathlib import Path
import re

import torch

from modules.util import setup_logging

setup_logging()
logger = logging.getLogger("default")

civit = Civit(cache_path=Path(path_manager.model_paths["cache_path"]) / Path("checkpoints"))

try:
    import modules.faceswapper_pipeline as faceswapper_pipeline

    logger.info("INFO: Faceswap enabled")
    state["faceswap_loaded"] = True
except:
    state["faceswap_loaded"] = False
import modules.sdxl_pipeline as sdxl_pipeline
import modules.template_pipeline as template_pipeline
import modules.upscale_pipeline as upscale_pipeline
import modules.search_pipeline as search_pipeline
import modules.huggingface_dl_pipeline as huggingface_dl_pipeline
import modules.diffusers_pipeline as diffusers_pipeline
import modules.stl_pipeline as stl_pipeline
import modules.rembg_pipeline as rembg_pipeline
import modules.controlnet as controlnet
from modules.model_info import get_all_model_info

class NoPipeLine:
    pipeline_type = []

def update(gen_data):
    prompt = gen_data["prompt"] if "prompt" in gen_data else ""
    cn_settings = controlnet.get_settings(gen_data)
    cn_type = cn_settings["type"] if "type" in cn_settings else ""

    try:
        if prompt == "ruinedfooocuslogo":
            if (
                state["pipeline"] is None
                or "template" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = template_pipeline.pipeline()

        elif prompt.startswith("search:"):
            if (
                state["pipeline"] is None
                or "search" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = search_pipeline.pipeline()

        elif re.match(r"^\s*hf:", prompt):
            if (
                state["pipeline"] is None
                or "huggingface_dl" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = huggingface_dl_pipeline.pipeline()

        elif cn_type.lower() == "upscale":
            if (
                state["pipeline"] is None
                or "upscale" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = upscale_pipeline.pipeline()

        elif cn_type.lower() == "faceswap" and state["faceswap_loaded"]:
            if (
                state["pipeline"] is None
                or "faceswap" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = faceswapper_pipeline.pipeline()

        elif cn_type.lower() == "rembg":
            if (
                state["pipeline"] is None
                or "rembg" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = rembg_pipeline.pipeline()

        elif cn_type.lower() == "stl":
            if (
                state["pipeline"] is None
                or "stl" not in state["pipeline"].pipeline_type
            ):
                state["pipeline"] = stl_pipeline.pipeline()

        else:
            baseModel = None
            baseModelName = ""
            if "base_model_name" in gen_data:
                model_info = get_all_model_info().get_model(gen_data['base_model_name'])
                assert model_info is not None, f"Model {gen_data['base_model_name']} not found"
                # file = Path(path_manager.model_paths["modelfile_path"]) / Path(gen_data['base_model_name'])
                # baseModel = civit.get_model_base(civit.get_models_by_path(file))
                baseModel = model_info.base
                baseModelName = gen_data['base_model_name']
            if state["pipeline"] is None:
                state["pipeline"] = NoPipeLine()

            if baseModelName.startswith("🤗"):
                if (
                    state["pipeline"] is None
                    or "diffusers" not in state["pipeline"].pipeline_type
                ):
                    state["pipeline"] = diffusers_pipeline.pipeline()

            elif baseModel is not None:
                # Try with SDXL if we have an "Unknown" model.
                if (
                    baseModel in ["Playground v2", "Pony", "SD 3", "SD3", "SDXL", "SDXL 1.0", "SDXL Distilled", "SDXL Hyper", "SDXL Turbo", "Flux.1 D", "Flux.1 S", "Unknown", "Merge"]
                    and "sdxl" not in state["pipeline"].pipeline_type
                ):
                    state["pipeline"] = sdxl_pipeline.pipeline()

        if state["pipeline"] is None or len(state["pipeline"].pipeline_type) == 0:
            logger.warning(f"Warning: Using SDXL pipeline as fallback.")
            state["pipeline"] = sdxl_pipeline.pipeline()

        return state["pipeline"]
    except:
        # If things fail. Use the template pipeline that only returns a logo
        state["pipeline"] = template_pipeline.pipeline()
        return state["pipeline"]


def clear_pipeline():
    state["pipeline"] = None
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
