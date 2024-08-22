import numpy as np
import datetime
import random
import logging
import math
import os
import cv2
import time
from pathlib import Path

from typing import Optional
from urllib.parse import urlparse
import json

from PIL import Image

logger = logging.getLogger("uvicorn.error")


LANCZOS = (Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)


def erode_or_dilate(x, k):
    k = int(k)
    if k > 0:
        return cv2.dilate(x, kernel=np.ones(shape=(3, 3), dtype=np.uint8), iterations=k)
    if k < 0:
        return cv2.erode(x, kernel=np.ones(shape=(3, 3), dtype=np.uint8), iterations=-k)
    return x


def resample_image(im, width, height):
    im = Image.fromarray(im)
    im = im.resize((int(width), int(height)), resample=LANCZOS)
    return np.array(im)


def resize_image(im, width, height, resize_mode=1):
    """
    Resizes an image with the specified resize_mode, width, and height.

    Args:
        resize_mode: The mode to use when resizing the image.
            0: Resize the image to the specified width and height.
            1: Resize the image to fill the specified width and height, maintaining the aspect ratio, and then center the image within the dimensions, cropping the excess.
            2: Resize the image to fit within the specified width and height, maintaining the aspect ratio, and then center the image within the dimensions, filling empty with data from image.
        im: The image to resize.
        width: The width to resize the image to.
        height: The height to resize the image to.
    """

    im = Image.fromarray(im)

    def resize(im, w, h):
        return im.resize((w, h), resample=LANCZOS)

    if resize_mode == 0:
        res = resize(im, width, height)

    elif resize_mode == 1:
        ratio = width / height
        src_ratio = im.width / im.height

        src_w = width if ratio > src_ratio else im.width * height // im.height
        src_h = height if ratio <= src_ratio else im.height * width // im.width

        resized = resize(im, src_w, src_h)
        res = Image.new("RGB", (width, height))
        res.paste(resized, box=(width // 2 - src_w // 2, height // 2 - src_h // 2))

    else:
        ratio = width / height
        src_ratio = im.width / im.height

        src_w = width if ratio < src_ratio else im.width * height // im.height
        src_h = height if ratio >= src_ratio else im.height * width // im.width

        resized = resize(im, src_w, src_h)
        res = Image.new("RGB", (width, height))
        res.paste(resized, box=(width // 2 - src_w // 2, height // 2 - src_h // 2))

        if ratio < src_ratio:
            fill_height = height // 2 - src_h // 2
            if fill_height > 0:
                res.paste(resized.resize((width, fill_height), box=(0, 0, width, 0)), box=(0, 0))
                res.paste(resized.resize((width, fill_height), box=(0, resized.height, width, resized.height)), box=(0, fill_height + src_h))
        elif ratio > src_ratio:
            fill_width = width // 2 - src_w // 2
            if fill_width > 0:
                res.paste(resized.resize((fill_width, height), box=(0, 0, 0, height)), box=(0, 0))
                res.paste(resized.resize((fill_width, height), box=(resized.width, 0, resized.width, height)), box=(fill_width + src_w, 0))

    return np.array(res)


def get_shape_ceil(h, w):
    return math.ceil(((h * w) ** 0.5) / 64.0) * 64.0


def get_image_shape_ceil(im):
    H, W = im.shape[:2]
    return get_shape_ceil(H, W)


def set_image_shape_ceil(im, shape_ceil):
    shape_ceil = float(shape_ceil)

    H_origin, W_origin, _ = im.shape
    H, W = H_origin, W_origin
    
    for _ in range(256):
        current_shape_ceil = get_shape_ceil(H, W)
        if abs(current_shape_ceil - shape_ceil) < 0.1:
            break
        k = shape_ceil / current_shape_ceil
        H = int(round(float(H) * k / 64.0) * 64)
        W = int(round(float(W) * k / 64.0) * 64)

    if H == H_origin and W == W_origin:
        return im

    return resample_image(im, width=W, height=H)


def HWC3(x):
    assert x.dtype == np.uint8
    if x.ndim == 2:
        x = x[:, :, None]
    assert x.ndim == 3
    H, W, C = x.shape
    assert C == 1 or C == 3 or C == 4
    if C == 3:
        return x
    if C == 1:
        return np.concatenate([x, x, x], axis=2)
    if C == 4:
        color = x[:, :, 0:3].astype(np.float32)
        alpha = x[:, :, 3:4].astype(np.float32) / 255.0
        y = color * alpha + 255.0 * (1.0 - alpha)
        y = y.clip(0, 255).astype(np.uint8)
        return y


def join_prompts(*args, **kwargs):
    prompts = [str(x) for x in args if str(x) != ""]
    if len(prompts) == 0:
        return ""
    if len(prompts) == 1:
        return prompts[0]
    return ', '.join(prompts)


def get_wildcard_files():
    directories = ["wildcards", "wildcards_official"]
    files = []

    for directory in directories:
        for file in Path(directory).rglob("*.txt"):
            name = file.stem
            if name not in files:
                files.append(name)

    onebutton = [
        "onebuttonprompt",
        "onebuttonsubject",
        "onebuttonhumanoid",
        "onebuttonmale",
        "onebuttonfemale",
        "onebuttonanimal",
        "onebuttonobject",
        "onebuttonlandscape",
        "onebuttonconcept",
        "onebuttonartist",
        "onebutton1girl",
        "onebutton1boy",
        "onebuttonfurry",
    ]
    both = files + onebutton
    return both


def model_hash(filename):
    """old hash that only looks at a small part of the file and is prone to collisions"""
    try:
        with open(filename, "rb") as file:
            import hashlib

            m = hashlib.sha256()
            file.seek(0x100000)
            m.update(file.read(0x10000))
            shorthash = m.hexdigest()[0:8]
            return shorthash
    except FileNotFoundError:
        return "NOFILE"
    except Exception:
        return "NOHASH"


def generate_temp_filename(folder="./outputs/", extension="png"):
    current_time = datetime.datetime.now()
    date_string = current_time.strftime("%Y-%m-%d")
    time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    random_number = random.randint(1000, 9999)
    filename = f"{time_string}_{random_number}.{extension}"
    result = Path(folder) / date_string / filename
    return date_string, result.absolute(), filename


def get_files_from_folder(folder_path, exensions=None, name_filter=None):
    if not os.path.isdir(folder_path):
        raise ValueError("Folder path is not a valid directory.")

    filenames = []

    for root, dirs, files in os.walk(folder_path):
        relative_path = os.path.relpath(root, folder_path)
        if relative_path == ".":
            relative_path = ""
        for filename in files:
            _, file_extension = os.path.splitext(filename)
            if (exensions == None or file_extension.lower() in exensions) and (name_filter == None or name_filter in _):
                path = os.path.join(relative_path, filename)
                filenames.append(path)

    return sorted(filenames, key=lambda x: -1 if os.sep in x else 1)


def load_keywords(lora):
    from shared import path_manager
    filename = Path(
        path_manager.model_paths["cache_path"] / "loras" / Path(lora).name
    ).with_suffix(".txt")
    try:
        with open(filename, "r") as file:
            data = file.read()
        return data
    except FileNotFoundError:
        return " "

def _get_model_hashes(cache_path, not_found=None):
    hashes = {
        "AutoV1": "",
        "AutoV2": "",
        "SHA256": "",
        "CRC32": "",
        "BLAKE3": "",
        "AutoV3": ""
    }
    filename = cache_path.with_suffix(".json")
    if Path(filename).is_file():
        try:
            with open(filename) as f:
                data = json.load(f)
        except:
            print(f"ERROR: model {cache_path} is missing json-file")
            data = {}
        if "files" not in data:
            data = {"files": [{"hashes": {}}]}
        hashes.update(data['files'][0]['hashes'])
        return hashes
    else:
        if not_found:
            return not_found
        else:
            return hashes

def get_checkpoint_hashes(model):
    from shared import path_manager
    return _get_model_thumbnail(
        Path(path_manager.model_paths["cache_path"] / "checkpoints" / Path(model).name)
    )

def get_lora_hashes(model):
    from shared import path_manager
    return _get_model_hashes(
        Path(path_manager.model_paths["cache_path"] / "loras" / Path(model).name)
    )

def _get_model_thumbnail(cache_path, not_found: str | None ="html/warning.png"):
    suffixes = [".jpeg", ".jpg", ".png", ".gif"]
    for suffix in suffixes:
        filename = cache_path.with_suffix(suffix)
        if Path(filename).is_file():
            return filename
    else:
        return not_found

def get_model_thumbnail(model):
    from shared import path_manager
    res = _get_model_thumbnail(
        Path(path_manager.model_paths["cache_path"] / "checkpoints" / Path(model).name),
        not_found=None
    )
    if res is not None:
        return res
    res = _get_model_thumbnail(
        Path(path_manager.model_paths["cache_path"] / "loras" / Path(model).name),
        not_found=None
    )
    if res is not None:
        return res
    else:
        return "html/warning.png"

def get_checkpoint_thumbnail(model):
    from shared import path_manager
    if Path(model).suffix == ".merge":
        not_found="html/merge.jpeg"
    else:
        not_found="html/warning.jpeg"

    return _get_model_thumbnail(
        Path(path_manager.model_paths["cache_path"] / "checkpoints" / Path(model).name),
        not_found=not_found
    )


def get_lora_thumbnail(model):
    from shared import path_manager
    return _get_model_thumbnail(
        Path(path_manager.model_paths["cache_path"] / "loras" / Path(model).name)
    )

def load_file_from_url(
    url: str,
    *,
    model_dir: str,
    progress: bool = True,
    file_name: Optional[str] = None,
) -> str:
    """Download a file from `url` into `model_dir`, using the file present if possible.

    Returns the path to the downloaded file.
    """
    Path(model_dir).mkdir(parents=True, exist_ok=True)
    if not file_name:
        parts = urlparse(url)
        file_name = Path(parts.path).stem

    for file in Path(model_dir).glob("**/*"):
        if file.name == file_name:
            cached_file = file
            return str(cached_file)

    cached_file = Path(model_dir) / file_name
    if not cached_file.exists():
        print(f'Downloading: "{url}" to {cached_file}\n')
        from torch.hub import download_url_to_file

        download_url_to_file(url, cached_file.absolute().as_posix(), progress=progress)
    return str(cached_file)


class TimeIt:
    def __init__(self, text=""):
        self.text = text

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        logger.info(f"[TimeIt] Time taken: {self.interval:0.2f} seconds {self.text}")


def remove_empty_str(items, default=None):
    items = [x for x in items if x != ""]
    if len(items) == 0 and default is not None:
        return [default]
    return items


def get_model_filename_given_binary_filename(binary_filename: str):
    original_filename = binary_filename
    if not original_filename.endswith(".safetensors"):
        binary_filename = original_filename + ".safetensors"
    if os.path.exists(binary_filename):
        return binary_filename
    if not os.path.exists(original_filename):
        return original_filename
    os.symlink(os.path.basename(original_filename), binary_filename)
    return binary_filename
