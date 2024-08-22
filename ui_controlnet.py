import modules.controlnet as controlnet
from modules.controlnet import (
    cn_options,
    load_cnsettings,
    save_cnsettings,
    NEWCN,
)
import gradio as gr
from shared import add_ctrl, path_manager
import ui_evolve


def add_controlnet_tab(main_view, inpaint_view, prompt, image_number, run_event):
    with gr.Tab(label="PowerUp"):
        with gr.Row():
            cn_selection = gr.Dropdown(
                label="Cheat Code",
                choices=["None"] + list(cn_options.keys()) + [NEWCN],
                value="None",
            )
            add_ctrl("cn_selection", cn_selection)

        cn_name = gr.Textbox(
            show_label=False,
            placeholder="Name",
            interactive=True,
            visible=False,
        )
        cn_save_btn = gr.Button(
            value="Save",
            visible=False,
        )

        cn_type = gr.Dropdown(
            label="Type",
            choices=map(lambda x: x.capitalize(), controlnet.controlnet_models.keys()),
            value=list(controlnet.controlnet_models.keys())[0].capitalize(),
            visible=False,
        )
        add_ctrl("cn_type", cn_type)

        cn_edge_low = gr.Slider(
            label="Edge (low)",
            minimum=0.0,
            maximum=1.0,
            step=0.01,
            value=0.2,
            visible=False,
        )
        add_ctrl("cn_edge_low", cn_edge_low)

        cn_edge_high = gr.Slider(
            label="Edge (high)",
            minimum=0.0,
            maximum=1.0,
            step=0.01,
            value=0.8,
            visible=False,
        )
        add_ctrl("cn_edge_high", cn_edge_high)

        cn_start = gr.Slider(
            label="Start",
            minimum=0.0,
            maximum=1.0,
            step=0.01,
            value=0.0,
            visible=False,
        )
        add_ctrl("cn_start", cn_start)

        cn_stop = gr.Slider(
            label="Stop",
            minimum=0.0,
            maximum=1.0,
            step=0.01,
            value=1.0,
            visible=False,
        )
        add_ctrl("cn_stop", cn_stop)

        cn_strength = gr.Slider(
            label="Strength",
            minimum=0.0,
            maximum=2.0,
            step=0.01,
            value=1.0,
            visible=False,
        )
        add_ctrl("cn_strength", cn_strength)

        cn_upscaler = gr.Dropdown(
            label=f"Upscaler",
            show_label=False,
            choices=["None"] + path_manager.upscaler_filenames,
            value="None",
            visible=False,
        )
        add_ctrl("cn_upscale", cn_upscaler)

        cn_outputs = [
            cn_name,
            cn_save_btn,
            cn_type,
        ]
        cn_sliders = [
            cn_start,
            cn_stop,
            cn_strength,
            cn_edge_low,
            cn_edge_high,
            cn_upscaler,
        ]

        @cn_selection.change(
            inputs=[cn_selection], outputs=[cn_name] + cn_outputs + cn_sliders
        )
        def cn_changed(selection):
            if selection != NEWCN:
                return [gr.update(visible=False)] + [gr.update(visible=False)] * len(
                    cn_outputs + cn_sliders
                )
            else:
                return [gr.update(value="")] + [gr.update(visible=True)] * len(
                    cn_outputs + cn_sliders
                )

        @cn_type.change(
            inputs=[cn_type],
            outputs=cn_sliders,
        )
        def cn_type_changed(selection):
            # cn_start,cn_stop,cn_strength,cn_edge_low,cn_edge_high, cn_upscaler
            slider_states = {
                "canny": [True, True, True, True, True, False],
                "img2img": [False, False, True, False, False, False],
                "default": [True, True, True, False, False, False],
                "upscale": [False, False, False, False, False, True],
                "faceswap": [False, False, False, False, False, False],
            }
            if selection.lower() in slider_states:
                show = slider_states[selection.lower()]
            else:
                show = slider_states["default"]

            result = []
            for vis in show:
                result += [gr.update(visible=vis)]

            return result

        @cn_save_btn.click(
            inputs=cn_outputs + cn_sliders,
            outputs=[cn_selection],
        )
        def cn_save(
            cn_name,
            cn_save_btn,
            cn_type,
            cn_start,
            cn_stop,
            cn_strength,
            cn_edge_low,
            cn_edge_high,
            upscale_model,
        ):
            if cn_name != "":
                cn_options = load_cnsettings()
                opts = {
                    "type": cn_type.lower(),
                    "start": cn_start,
                    "stop": cn_stop,
                    "strength": cn_strength,
                    "upscaler": cn_upscaler,
                }
                if cn_type.lower() == "canny":
                    opts.update(
                        {
                            "edge_low": cn_edge_low,
                            "edge_high": cn_edge_high,
                        }
                    )
                cn_options[cn_name] = opts
                save_cnsettings(cn_options)
                choices = list(cn_options.keys()) + [NEWCN]
                return gr.update(choices=choices, value=cn_name)
            else:
                return gr.update()

        input_image = gr.Image(
            label="Input image",
            type="pil",
            visible=True,
        )
        add_ctrl("input_image", input_image)
        inpaint_toggle = gr.Checkbox(label="Inpainting", value=False)

        add_ctrl("inpaint_toggle", inpaint_toggle)

        @inpaint_toggle.change(
            inputs=[inpaint_toggle, main_view], outputs=[main_view, inpaint_view]
        )
        def inpaint_checked(r, test):
            if r:
                return {
                    main_view: gr.update(visible=False),
                    inpaint_view: gr.update(visible=True, value=test),
                }
            else:
                return {
                    main_view: gr.update(visible=True),
                    inpaint_view: gr.update(visible=False),
                }

        ui_evolve.add_evolve_tab(prompt, image_number, run_event)

    return inpaint_toggle

