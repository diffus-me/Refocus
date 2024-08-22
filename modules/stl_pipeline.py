from collections.abc import Callable

import modules.async_worker as worker

from modules.util import generate_temp_filename
import shared

import torch
import numpy as np
import os
import math
import rembg
from PIL import Image
from pathlib import Path

from sf3d.system import SF3D
from sf3d.utils import remove_background, resize_foreground

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh

class pipeline:
    pipeline_type = ["stl"]
    model_hash = ""

    pipeline = None
    model = None
    device = "cuda:0"

    # Optional function
    def parse_gen_data(self, gen_data):
        return gen_data

    def load_base_model(self, name):
        if self.pipeline is not None:
            return

        self.device = torch.device('cuda')
        if not torch.cuda.is_available():
            self.device = "cpu"

        print('Loading SF3D model ...')

        os.environ["HF_HOME"] = "models/diffusers_cache"
        self.pipeline = SF3D.from_pretrained(
            "stabilityai/stable-fast-3d",
            config_name="config.yaml",
            weight_name="model.safetensors",
        )
        self.pipeline.to(self.device)
        self.pipeline.eval()

        print('Loading Finished!')
        return

    def load_keywords(self, lora):
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
        # GIFs parameters
        frame_count = 25
        duration_frame = 0.2

        # Visualization parameters
        init_angle = 0
        elevation = 20
        rotation_axises = [1.0, 0.0, 0.0]
        rotation_angle = -90
        x_offset = 0
        y_offset = 0
        z_offset = 0

        if gen_data["prompt"].startswith("token:"):
            from huggingface_hub import login
            login(token=gen_data["prompt"].split("token:")[1].strip())

        if progressbar:
            progressbar(1, "Removing background ...")

        rembg_session = rembg.new_session()
        input_image = remove_background(
            input_image.convert("RGBA"), rembg_session
        )
        input_image = resize_foreground(input_image, 0.85)

        if callback is not None:
            callback(0, 0, 0, 0, input_image)

        stl_filename = generate_temp_filename(
            folder=shared.path_manager.model_paths["temp_outputs_path"],
            extension="stl",
        )
        images = generate_temp_filename(
            folder=shared.path_manager.model_paths["temp_outputs_path"],
            extension="gif",
        )
        dir_path = Path(stl_filename).parent
        dir_path.mkdir(parents=True, exist_ok=True)

        if progressbar:
            progressbar(1, "Running SF3D ...")

        torch.cuda.reset_peak_memory_stats()
        with torch.no_grad():
            texture_resolution = 1024
            remesh_option = "none" # choices=["none", "triangle", "quad"],
            sf3d_mesh, glob_dict = self.pipeline.run_image(
                [input_image],
                bake_resolution=texture_resolution,
                remesh=remesh_option,
            )

        if progressbar:
            progressbar(1, "Export STL ...")
        sf3d_mesh.export(stl_filename)
        print("Peak Memory:", torch.cuda.max_memory_allocated() / 1024 / 1024, "MB")

        print("Loading STL")
        stl_mesh = mesh.Mesh.from_file(stl_filename)

        # Rotate
        stl_mesh.rotate(rotation_axises, math.radians(rotation_angle))
    
        print("Creating GIF")
        # Center the STL
        x_min = stl_mesh.vectors[:,:,0].min()
        x_max = stl_mesh.vectors[:,:,0].max()
        y_min = stl_mesh.vectors[:,:,1].min()
        y_max = stl_mesh.vectors[:,:,1].max()
        z_min = stl_mesh.vectors[:,:,2].min()
        z_max = stl_mesh.vectors[:,:,2].max() 

        x_center_offset = (x_max + x_min)/2.0
        y_center_offset = (y_max + y_min)/2.0
        z_center_offset = (z_max + z_min)/2.0

        stl_mesh.vectors[:,:,0] = stl_mesh.vectors[:,:,0] - x_center_offset - x_offset
        stl_mesh.vectors[:,:,1] = stl_mesh.vectors[:,:,1] - y_center_offset - y_offset
        stl_mesh.vectors[:,:,2] = stl_mesh.vectors[:,:,2] - z_center_offset - z_offset
    
        # Create a new plot
        figure = plt.figure()
        axes = figure.add_subplot(projection='3d')

        # Add STL vectors to the plot
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors,color="cyan"))
        axes.add_collection3d(mplot3d.art3d.Line3DCollection(stl_mesh.vectors,color="black",linewidth=0.1))
        #axes.view_init(elev=35., azim=-45)

        # Auto scale to the mesh size
        scale = stl_mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)

        # Deactivate Axes
        plt.axis('off')

        if progressbar:
            progressbar(1, "Create GIF ...")

        frames = []
        #for i in range(frame_count):    
        i = 5
        # Rotate the view
        axes.view_init(elev=elevation, azim=init_angle + 360/frame_count*i)
        x = figure.canvas.print_to_buffer()
        frames.append(Image.frombytes('RGBA', x[1], x[0]))

        # Save the images as a GIF using imageio
        os.makedirs(os.path.dirname(images), exist_ok=True)
        frames[0].save(
            images,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=duration_frame,
            loop=0,
        )

        return [images]
