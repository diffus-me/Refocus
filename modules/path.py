from pathlib import Path
import json
import threading
from modules.civit import Civit
import time
from modules.model_info import get_all_model_info


class PathManager:
    DEFAULT_PATHS = {
        "path_checkpoints": "../models/checkpoints/",
        "path_diffusers": "../models/diffusers/",
        "path_diffusers_cache": "../models/diffusers_cache/",
        "path_loras": "../models/loras/",
        "path_controlnet": "../models/controlnet/",
        "path_vae_approx": "../models/vae_approx/",
        "path_preview": "../outputs/preview.jpg",
        "path_faceswap": "../models/faceswap/",
        "path_upscalers": "../models/upscale_models",
        "path_outputs": "../outputs/",
        "path_clip": "../models/clip/",
        "path_cache": "../cache/",
    }

    EXTENSIONS = [".pth", ".ckpt", ".bin", ".safetensors", ".merge"]

    civit_worker_folders = []

    def __init__(self):
        self.paths = self.load_paths()
        self.model_paths = self.get_model_paths()
        self.default_model_names = self.get_default_model_names()
        self.update_all_model_names()

    def load_paths(self):
        paths = self.DEFAULT_PATHS.copy()
        settings_path = Path("settings/paths.json")
        if settings_path.exists():
            with settings_path.open() as f:
                paths.update(json.load(f))
        for key in self.DEFAULT_PATHS:
            if key not in paths:
                paths[key] = self.DEFAULT_PATHS[key]
        with settings_path.open("w") as f:
            json.dump(paths, f, indent=2)
        return paths

    def get_model_paths(self):
        return {
            "modelfile_path": self.get_abspath_folder(self.paths["path_checkpoints"]),
            "diffusers_path": self.get_abspath_folder(self.paths["path_diffusers"]),
            "diffusers_cache_path": self.get_abspath_folder(self.paths["path_diffusers_cache"]),
            "lorafile_path": self.get_abspath_folder(self.paths["path_loras"]),
            "controlnet_path": self.get_abspath_folder(self.paths["path_controlnet"]),
            "vae_approx_path": self.get_abspath_folder(self.paths["path_vae_approx"]),
            "temp_outputs_path": self.get_abspath_folder(self.paths["path_outputs"]),
            "temp_preview_path": self.get_abspath(self.paths["path_preview"]),
            "faceswap_path": self.get_abspath_folder(self.paths["path_faceswap"]),
            "upscaler_path": self.get_abspath_folder(self.paths["path_upscalers"]),
            "clip_path": self.get_abspath_folder(self.paths["path_clip"]),
            "cache_path": self.get_abspath_folder(self.paths["path_cache"]),
        }

    def get_default_model_names(self):
        return {
            "default_base_model_name": "sd_xl_base_1.0_0.9vae.safetensors",
            "default_lora_name": "sd_xl_offset_example-lora_1.0.safetensors",
            "default_lora_weight": 0.5,
        }

    def get_abspath_folder(self, path):
        folder = self.get_abspath(path)
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        return folder

    def get_abspath(self, path):
        return Path(path) if Path(path).is_absolute() else Path(__file__).parent / path

    def civit_update_worker(self, folder_path, cache, isLora):
        try:
            import imageio.v3
        except:
            # Skip updates if we are missing imageio
            print(f"DEBUG: Skip CivitAI update")
            return
        if folder_path in self.civit_worker_folders:
            # Already working on this folder
            return
        if cache:
            cache_path = Path(self.model_paths["cache_path"] / cache)
        else:
            return
        self.civit_worker_folders.append(folder_path)
        civit = Civit(cache_path=cache_path.absolute().as_posix())
        for path in folder_path.rglob("*"):
            if path.suffix.lower() in self.EXTENSIONS:

                # get file name, add cache path change suffix
                cache_file = Path(cache_path / path.name)

                models = None
                has_preview = False

                suffixes = [".jpeg", ".jpg", ".png", ".gif"]
                thumbcheck = ""
                for suffix in suffixes:
                    thumbcheck = cache_file.with_suffix(suffix)
                    if Path(thumbcheck).is_file():
                        has_preview = True
                        break

                if not has_preview:
                    if models is None:
                        models = civit.get_models_by_path(str(path))
                    #print(f"Downloading model thumbnail for {Path(path).name} ({civit.get_model_base(models)} - {civit.get_model_type(models)})")
                    civit.get_image(models, thumbcheck)
                    time.sleep(1)

                txtcheck = cache_file.with_suffix(".txt")
                if isLora and not txtcheck.exists():
                    if models is None:
                        models = civit.get_models_by_path(str(path))
                    print(f"Downloading LoRA keywords for {Path(path).name} ({civit.get_model_base(models)} - {civit.get_model_type(models)})")
                    keywords = civit.get_keywords(models)
                    with open(txtcheck, "w") as f:
                        f.write(", ".join(keywords))
                    time.sleep(1)

        self.civit_worker_folders.remove(folder_path)

    def get_model_filenames(self, folder_path, cache=None, isLora=False):
        folder_path = Path(folder_path)
        if not folder_path.is_dir():
            raise ValueError(f"{folder_path} is not a valid directory.")
        threading.Thread(
            target=self.civit_update_worker,
            args=(
                folder_path,
                cache,
                isLora,
            ),
            daemon=True,
        ).start()
        filenames = []
        for path in folder_path.rglob("*"):
            if path.suffix.lower() in self.EXTENSIONS:
                if isLora:
                    txtcheck = path.with_suffix(".txt")
                    if txtcheck.exists():
                        fstats = txtcheck.stat()
                        if fstats.st_size > 0:
                            path = path.with_suffix(f"{path.suffix}")
                filenames.append(str(path.relative_to(folder_path)))
        # Return a sorted list, prepend names with 0 if they are in a folder or 1
        # if it is a plain file. This will sort folders above files in the dropdown
        return sorted(
            filenames,
            key=lambda x: f"0{x.casefold()}"
            if not str(Path(x).parent) == "."
            else f"1{x.casefold()}",
        )

    def get_diffusers_filenames(self, folder_path, cache=None, isLora=False):
        folder_path = Path(folder_path)
        if not folder_path.is_dir():
            raise ValueError(f"{folder_path} is not a valid directory.")
        filenames = []
        for path in folder_path.glob("*/*"):
#            if path.suffix.lower() in self.EXTENSIONS:
#                if isLora:
#                    txtcheck = path.with_suffix(".txt")
#                    if txtcheck.exists():
#                        fstats = txtcheck.stat()
#                        if fstats.st_size > 0:
#                            path = path.with_suffix(f"{path.suffix}")
            filenames.append(f"🤗:{path.relative_to(folder_path)}")
        return sorted(
            filenames,
            key=lambda x: f"0{x.casefold()}"
            if not str(Path(x).parent) == "."
            else f"1{x.casefold()}",
        )

    def update_all_model_names(self):
        all_model_info = get_all_model_info()
        self.model_filenames = [model_name for model_name in all_model_info.checkpoint_models]
        #self.model_filenames = self.get_model_filenames(
        #    self.model_paths["modelfile_path"],
        #    cache="checkpoints"
        #) + self.get_diffusers_filenames(
        #    self.model_paths["diffusers_path"],
        #    cache="checkpoints"
        #)
        self.lora_filenames = [model_name for model_name in all_model_info.lora_models]
        #self.lora_filenames = self.get_model_filenames(
        #    self.model_paths["lorafile_path"], 
        #    cache="loras",
        #    isLora=True
        #)
        self.upscaler_filenames = self.get_model_filenames(
            self.model_paths["upscaler_path"]
        )

    def find_lcm_lora(self):
        filename = "lcm-lora-sdxl.safetensors"
        model_info = get_all_model_info().get_model(filename)
        if model_info:
            return filename
        return None
        # path = Path(self.model_paths["lorafile_path"])
        # filename = "lcm-lora-sdxl.safetensors"
        # for child in path.rglob(filename):
        #     if child.name == filename:
        #         return child.relative_to(path)
