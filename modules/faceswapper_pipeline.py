from collections.abc import Callable
import os
import sys
import cv2
import re
from shared import path_manager
import modules.async_worker as worker
from tqdm import tqdm
import tempfile

from modules.settings import default_settings
from modules.util import generate_temp_filename

from PIL import Image
import imageio.v3 as iio
import numpy as np
import torch
import insightface
#import onnxruntime
import gfpgan
from facexlib.utils.face_restoration_helper import FaceRestoreHelper

# Requirements:
# insightface==0.7.3
# onnxruntime-gpu==1.16.1
# imageio==2.31.6
# gfpgan==1.3.8
# add to settings/powerup.json
#
#  "Faceswap": {
#    "type": "faceswap"
#  }
#
# Models in models/faceswap/
# https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
# and inswapper_128.onnx from where you can find it

class pipeline:
    pipeline_type = ["faceswap"]

    analyser_model = None
    analyser_hash = ""
    swapper_model = None
    swapper_hash = ""
    gfpgan_model = None

    def load_base_model(self, name):
        model_name = "inswapper_128.onnx"
        if not self.swapper_hash == model_name:
            print(f"Loading swapper model: {model_name}")
            model_path = os.path.join(path_manager.model_paths["faceswap_path"], model_name)
            try:
                with open(os.devnull, "w") as sys.stdout:
                    self.swapper_model = insightface.model_zoo.get_model(
                        model_path,
                        download=False,
                        download_zip=False,
                    )
                    self.swapper_hash = model_name
                sys.stdout = sys.__stdout__
            except:
                print(f"Failed loading model! {model_path}")

        model_name = "buffalo_l"
        det_thresh = 0.5
        if not self.analyser_hash == model_name:
            print(f"Loading analyser model: {model_name}")
            try:
                with open(os.devnull, "w") as sys.stdout:
                    self.analyser_model = insightface.app.FaceAnalysis(name=model_name)
                    self.analyser_model.prepare(
                        ctx_id=0, det_thresh=det_thresh, det_size=(640, 640)
                    )
                    self.analyser_hash = model_name
                sys.stdout = sys.__stdout__
            except:
                print(f"Failed loading model! {model_name}")

    def load_gfpgan_model(self):
        if self.gfpgan_model is None:
            channel_multiplier = 2

            model_name = "GFPGANv1.4.pth"
            model_path = os.path.join(path_manager.model_paths["faceswap_path"], model_name)

            # https://github.com/TencentARC/GFPGAN/blob/master/inference_gfpgan.py
            self.gfpgan_model = gfpgan.GFPGANer
            self.gfpgan_model.bg_upsampler = None
            # initialize model
            self.gfpgan_model.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )

            upscale = 2
            self.gfpgan_model.face_helper = FaceRestoreHelper(
                upscale,
                det_model="retinaface_resnet50",
                model_rootpath=path_manager.model_paths["faceswap_path"],
            )
            # face_size=512,
            # crop_ratio=(1, 1),
            # save_ext='png',
            # use_parse=True,
            # device=self.device,

            self.gfpgan_model.gfpgan = gfpgan.GFPGANv1Clean(
                out_size=512,
                num_style_feat=512,
                channel_multiplier=channel_multiplier,
                decoder_load_path=None,
                fix_decoder=False,
                num_mlp=8,
                input_is_latent=True,
                different_w=True,
                narrow=1,
                sft_half=True,
            )

            loadnet = torch.load(model_path)
            if "params_ema" in loadnet:
                keyname = "params_ema"
            else:
                keyname = "params"
            self.gfpgan_model.gfpgan.load_state_dict(loadnet[keyname], strict=True)
            self.gfpgan_model.gfpgan.eval()
            self.gfpgan_model.gfpgan = self.gfpgan_model.gfpgan.to(
                self.gfpgan_model.device
            )

    def load_keywords(self, lora):
        return ""

    def load_loras(self, loras):
        return

    def refresh_controlnet(self, name=None):
        return

    def clean_prompt_cond_caches(self):
        return

    def swap_faces(self, original_image, input_faces, out_faces):
        idx = 0
        for out_face in out_faces:
            original_image = self.swapper_model.get(
                original_image,
                out_face,
                input_faces[idx % len(input_faces)],
                paste_back=True,
            )
            idx += 1
        return original_image

    def restore_faces(self, image):
        self.load_gfpgan_model()

        image_bgr = image[:, :, ::-1]
        _cropped_faces, _restored_faces, gfpgan_output_bgr = self.gfpgan_model.enhance(
            self.gfpgan_model,
            image_bgr,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=0.5,
        )
        image = gfpgan_output_bgr[:, :, ::-1]

        return image

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

        input_image = cv2.cvtColor(np.asarray(input_image), cv2.COLOR_RGB2BGR)
        input_faces = sorted(
            self.analyser_model.get(input_image), key=lambda x: x.bbox[0]
        )

        prompt = gen_data["prompt"].strip()
        if re.fullmatch("https?://.*\.gif", prompt, re.IGNORECASE) is not None:
            x = iio.immeta(prompt)
            duration = x["duration"]
            loop = x["loop"]
            gif = cv2.VideoCapture(prompt)

            # Swap
            in_imgs = []
            out_imgs = []
            while True:
                ret, frame = gif.read()
                if not ret:
                    break
                in_imgs.append(frame)

            with tqdm(total=len(in_imgs), desc="Groop", unit="frames") as progress:
                i=0
                steps=len(in_imgs)
                for frame in in_imgs:
                    out_faces = sorted(
                        self.analyser_model.get(frame), key=lambda x: x.bbox[0]
                    )
                    frame = self.swap_faces(frame, input_faces, out_faces)
                    out_imgs.append(
                        Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    )
                    i+=1
                    callback(i, 0, 0, steps, out_imgs[-1])
                    progress.update(1)
            images = generate_temp_filename(
                folder=path_manager.model_paths["temp_outputs_path"], extension="gif"
            )
            os.makedirs(os.path.dirname(images), exist_ok=True)
            out_imgs[0].save(
                images,
                save_all=True,
                append_images=out_imgs[1:],
                optimize=True,
                duration=duration,
                loop=loop,
            )
        else:
            output_image = cv2.imread(main_view)
            output_faces = sorted(
                self.analyser_model.get(output_image), key=lambda x: x.bbox[0]
            )
            result_image = self.swap_faces(output_image, input_faces, output_faces)
            result_image = self.restore_faces(result_image)
            images = Image.fromarray(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))

        return [images]
