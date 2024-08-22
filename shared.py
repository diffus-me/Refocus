from modules.performance import PerformanceSettings
from modules.resolutions import ResolutionSettings
from modules.path import PathManager

gradio_root = None
last_stop = None

state = {"preview_image": None, "ctrls_name": [], "ctrls_obj": [], "pipeline": None}

wildcards = None
try:
    from transformers import CLIPTokenizer
    tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
except:
    print("DEBUG: No tokenizer in shared.py")
    tokenizer = None

performance_settings = PerformanceSettings()
resolution_settings = ResolutionSettings()

path_manager = PathManager()


def add_ctrl(name, obj):
    state["ctrls_name"] += [name]
    state["ctrls_obj"] += [obj]
