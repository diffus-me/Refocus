import torch
from clip_interrogator import Config, Interrogator
from PIL import Image
import json
from shared import state, path_manager


def look(image, prompt, gr):
    if prompt != "":
        return prompt
    try:
        info = image.info
        params = info.get("parameters", "")
        text = json.dumps(json.loads(params))
    except:
        text = "Lets interrogate"

        # Unload models, if needed?
        # state["pipeline"] = None
        gr.Info("Creating Your Prompt")

        conf = Config(
            device=torch.device("cuda"),
            clip_model_name="ViT-L-14/openai",
            cache_path=path_manager.model_paths["clip_path"],
        )
        conf.apply_low_vram_defaults()

        i = Interrogator(conf)
        text = i.interrogate(image)

    return text
