import ldm_patched.modules.args_parser as args_parser


args_parser.parser.add_argument("--share", action='store_true', help="Set whether to share on Gradio.")
args_parser.parser.add_argument("--preset", type=str, default=None, help="Apply specified UI preset.")

args_parser.parser.add_argument("--language", type=str, default='default',
                                help="Translate UI using json files in [language] folder. "
                                  "For example, [--language example] will use [language/example.json] for translation.")

# For example, https://github.com/lllyasviel/Fooocus/issues/849
args_parser.parser.add_argument("--disable-offload-from-vram", action="store_true",
                                help="Force loading models to vram when the unload can be avoided. "
                                  "Some Mac users may need this.")

args_parser.parser.add_argument("--theme", type=str, help="launches the UI with light or dark theme", default=None)
args_parser.parser.add_argument("--disable-image-log", action='store_true',
                                help="Prevent writing images and logs to hard drive.")

args_parser.parser.add_argument("--disable-analytics", action='store_true',
                                help="Disables analytics for Gradio", default=False)

args_parser.parser.set_defaults(
    disable_cuda_malloc=True,
    in_browser=True,
    port=None
)
args_parser.parser.add_argument("--lazy", action='store_true', default=False,
                                help="Only start worker thread when there are tasks in the queue.")
args_parser.parser.add_argument("--no-gradio", action='store_true', default=False,
                                help="Disable gradio from lauching if required.")

args_parser.parser.add_argument("--logging-level", type=str, help="logging level", default='INFO')
args_parser.parser.add_argument("--logging-file-dir", type=str, help="Where to save logs file", default='')

args_parser.args = args_parser.parser.parse_args()

# (Disable by default because of issues like https://github.com/lllyasviel/Fooocus/issues/724)
args_parser.args.always_offload_from_vram = not args_parser.args.disable_offload_from_vram

if args_parser.args.disable_analytics:
    import os
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

args = args_parser.args
