import logging
import os
import sys
import ssl

print('[System ARGV] ' + str(sys.argv))

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
os.environ["GRADIO_SERVER_PORT"] = "7865"

ssl._create_default_https_context = ssl._create_unverified_context


import platform
import fooocus_version
import warnings
from pathlib import Path
import ssl

from build_launcher import build_launcher
from modules import config
from modules import model_info


ssl._create_default_https_context = ssl._create_unverified_context

warnings.filterwarnings("ignore", category=FutureWarning, module="insightface")
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision")
warnings.filterwarnings("ignore", category=UserWarning, module="gradio")
warnings.filterwarnings("ignore", category=UserWarning, module="torchsde")
warnings.filterwarnings("ignore", category=UserWarning)

warnings.filterwarnings(
    "ignore", category=UserWarning, module="torchvision.transforms.functional_tensor"
)
warnings.filterwarnings(
    "ignore", category=UserWarning, message="TypedStorage is deprecated"
)

from modules.launch_util import (
    is_installed,
    run,
    python,
    run_pip,
    repo_dir,
    git_clone,
    requirements_met,
    script_path,
    dir_repos,
)

REINSTALL_ALL = False
if os.path.exists("reinstall"):
    REINSTALL_ALL = True


def prepare_environment():
    torch_index_url = os.environ.get(
        "TORCH_INDEX_URL", "https://download.pytorch.org/whl/cu121"
    )
    torch_command = os.environ.get(
        "TORCH_COMMAND",
        f"pip install torch==2.2.2 torchvision==0.17.2 --extra-index-url {torch_index_url}",
    )
    insightface_package = os.environ.get(
        "INSIGHTFACE_PACKAGE",
        f"https://github.com/Gourieff/sd-webui-reactor/raw/main/example/insightface-0.7.3-cp310-cp310-win_amd64.whl",
    )
    requirements_file = os.environ.get("REQS_FILE", "requirements_versions.txt")

    xformers_package = os.environ.get("XFORMERS_PACKAGE", "xformers==0.0.26.post1")

    comfy_repo = os.environ.get(
        "COMFY_REPO", "https://github.com/comfyanonymous/ComfyUI"
    )
    comfy_commit_hash = os.environ.get(
        "COMFY_COMMIT_HASH", "39fb74c5bd13a1dccf4d7293a2f7a755d9f43cbd"
    )
    sf3d_repo = os.environ.get(
        "SF3D_REPO", "https://github.com/Stability-AI/stable-fast-3d.git"
    )
    sf3d_commit_hash = os.environ.get(
        "SF3D_COMMIT_HASH", "070ece138459e38e1fe9f54aa19edb834bced85e"
    )

    print(f"Python {sys.version}")
    print(f"RuinedFooocus version: {fooocus_version.version}")

    comfyui_name = "ComfyUI-from-StabilityAI-Official"
    git_clone(comfy_repo, repo_dir(comfyui_name), "Comfy Backend", comfy_commit_hash)
    path = Path(script_path) / dir_repos / comfyui_name
    sys.path.append(str(path))

    sf3d_name = "stable-fast-3d"
    git_clone(sf3d_repo, repo_dir(sf3d_name), "Stable Fast 3D", sf3d_commit_hash)
    path = Path(script_path) / dir_repos / "stable-fast-3d"
    sys.path.append(str(path))

    if REINSTALL_ALL or not is_installed("torch") or not is_installed("torchvision"):
        run(
            f'"{python}" -m {torch_command}',
            "Installing torch and torchvision",
            "Couldn't install torch",
            live=True,
        )

    if REINSTALL_ALL or not is_installed("xformers"):
        if platform.system() == "Windows":
            if platform.python_version().startswith("3.10"):
                run_pip(
                    f"install -U -I --no-deps {xformers_package}", "xformers", live=True
                )
            else:
                print(
                    "Installation of xformers is not supported in this version of Python."
                )
                print(
                    "You can also check this and build manually: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Xformers#building-xformers-on-windows-by-duckness"
                )
                if not is_installed("xformers"):
                    exit(0)
        elif platform.system() == "Linux":
            run_pip(f"install -U -I --no-deps {xformers_package}", "xformers")

    if REINSTALL_ALL or not requirements_met(requirements_file):
        print("This next step may take a while")
        run_pip(f'install -r "{requirements_file}"', "requirements")

    return


model_filenames = [
    (
        "sd_xl_base_1.0_0.9vae.safetensors",
        "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0_0.9vae.safetensors",
    ),
]

lora_filenames = [
    (
        "sd_xl_offset_example-lora_1.0.safetensors",
        "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors",
    ),
    (
        "lcm-lora-sdxl.safetensors",
        "https://huggingface.co/latent-consistency/lcm-lora-sdxl/resolve/main/pytorch_lora_weights.safetensors",
    ),
    (
        "lcm-lora-ssd-1b.safetensors",
        "https://huggingface.co/latent-consistency/lcm-lora-ssd-1b/resolve/main/pytorch_lora_weights.safetensors",
    ),
]

vae_approx_filenames = [
    (
        "taesdxl_decoder",
        "https://github.com/madebyollin/taesd/raw/main/taesdxl_decoder.pth",
    ),
    ('xlvaeapp.pth', 'https://huggingface.co/lllyasviel/misc/resolve/main/xlvaeapp.pth'),
    ('vaeapp_sd15.pth', 'https://huggingface.co/lllyasviel/misc/resolve/main/vaeapp_sd15.pt'),
    ('xl-to-v1_interposer-v3.1.safetensors',
     'https://huggingface.co/lllyasviel/misc/resolve/main/xl-to-v1_interposer-v3.1.safetensors')
]

controlnet_filenames = [
    (
        "control-lora-canny-rank128.safetensors",
        "https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-canny-rank128.safetensors",
    ),
    (
        "control-lora-depth-rank128.safetensors",
        "https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-depth-rank128.safetensors",
    ),
    (
        "control-lora-recolor-rank128.safetensors",
        "https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-recolor-rank128.safetensors",
    ),
    (
        "control-lora-sketch-rank128-metadata.safetensors",
        "https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-sketch-rank128-metadata.safetensors",
    ),
]

upscaler_filenames = [
    (
        "4x-UltraSharp.pth",
        "https://huggingface.co/lokCX/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth",
    ),
]

magic_prompt_filenames = [
    (
        "pytorch_model.bin",
        "https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin",
    ),
]

layer_diffuse_filenames = [
    (
        "layer_xl_transparent_attn.safetensors",
        "https://huggingface.co/LayerDiffusion/layerdiffusion-v1/resolve/main/layer_xl_transparent_attn.safetensors",
    ),
    (
        "vae_transparent_decoder.safetensors",
        "https://huggingface.co/LayerDiffusion/layerdiffusion-v1/resolve/main/vae_transparent_decoder.safetensors",
    ),
]


def download_models(args):
    from modules.util import load_file_from_url
    from shared import path_manager

    for file_name, url in controlnet_filenames:
        load_file_from_url(
            url=url,
            model_dir=path_manager.model_paths["controlnet_path"],
            file_name=file_name,
        )
    for file_name, url in vae_approx_filenames:
        load_file_from_url(
            url=url,
            model_dir=path_manager.model_paths["vae_approx_path"],
            file_name=file_name,
        )
    for file_name, url in upscaler_filenames:
        load_file_from_url(
            url=url,
            model_dir=path_manager.model_paths["upscaler_path"],
            file_name=file_name,
        )
    for file_name, url in magic_prompt_filenames:
        load_file_from_url(
            url=url,
            model_dir="prompt_expansion",
            file_name=file_name,
        )
    for file_name, url in layer_diffuse_filenames:
        load_file_from_url(
            url=url,
            model_dir="models/layerdiffuse/",
            file_name=file_name,
        )

    load_file_from_url(
        url='https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin',
        model_dir=config.path_fooocus_expansion,
        file_name='pytorch_model.bin'
    )

    if args.disable_preset_download:
        print('Skipped model download.')
        return

    #for file_name, url in model_filenames:
    #    load_file_from_url(
    #        url=url,
    #        model_dir=path_manager.model_paths["modelfile_path"],
    #        file_name=file_name,
    #    )
    #for file_name, url in lora_filenames:
    #    load_file_from_url(
    #        url=url,
    #        model_dir=path_manager.model_paths["lorafile_path"],
    #        file_name=file_name,
    #    )
    return


def clear_comfy_args():
    argv = sys.argv
    sys.argv = [sys.argv[0]]
    import comfy.cli_args

    sys.argv = argv


def ini_args():
    from args_manager import args
    return args


def _config_logging(logging_level, logging_file_dir, component):
    level = logging.getLevelName(logging_level)
    logger_format = '%(asctime)s [%(levelname)s] (%(name)s:%(lineno)d): %(message)s'

    if logging_file_dir:
        import pathlib
        log_filename = pathlib.Path(logging_file_dir, f'{component}.log')
        logging.basicConfig(level=level,
                            filename=str(log_filename),
                            format=logger_format,
                            force=True)
    else:
        logging.basicConfig(level=level,
                            format=logger_format)


def launch(server_port: int = 0):
    import webui
    prepare_environment()
    if os.path.exists("reinstall"):
        os.remove("reinstall")

    clear_comfy_args()
    # cuda_malloc()
    build_launcher()
    args = ini_args()

    if args.gpu_device_id is not None:
        os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_device_id)
        print("Set device to:", args.gpu_device_id)

    _config_logging(args.logging_level, args.logging_file_dir, 'focus')

    download_models(args)

    model_info.download_models()
    model_info.update_model_list()

    webui.start(server_port)
