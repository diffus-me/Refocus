# Fooocus Update Logs

# 2.1.864

* New model list. See also discussions.

# 2.1.861 (requested update)

(2023 Dec 21) Hi all, the feature updating of Fooocus will be paused for about two or three weeks because we have some other workloads. See you soon and we will come back in mid or late Jan. However, you may still see updates if other collaborators are fixing bugs or solving problems.

* Show image preview in Style when mouse hover.

# 2.1.860 (requested update)

* Allow upload inpaint mask in developer mode.

# 2.1.857 (requested update)

* Begin to support 8GB AMD GPU on Windows.

# 2.1.854

* Add a button to copy parameters to clipboard in log.
* Allow users to load parameters directly by pasting parameters to prompt.

# 2.1.853

* Add Marc K3nt3L's styles. Thanks [Marc K3nt3L](https://github.com/K3nt3L)!

# 2.1.852

* New Log System: Log system now uses tables. If this is breaking some other browser extension or javascript developments, see also [use previous version](https://github.com/lllyasviel/Fooocus/discussions/1405).

# 2.1.846

* Many users reported that image quality is different from 2.1.824. We reviewed all codes and fixed several precision problems in 2.1.846.

# 2.1.843

* Many improvements to Canvas. Thanks CanvasZoom author!

# 2.1.841

* Backend maintain.
* Fix some potential frozen after model mismatch.
* Fix crash when cfg=1 when using anime preset.
* Added some guidelines for troubleshoot the "CUDA kernel errors asynchronously" problem.
* Fix inpaint device problem in `--always-gpu` mode.

# 2.1.839

* Maintained some computation codes in backend for efficiency.
* Added a note about Seed Breaking Change.

**Seed Breaking Change**: Note that 2.1.825-2.1.839 is seed breaking change. The computation float point is changed and some seeds may give slightly different results. The minor change in 2.1.825-2.1.839 do not influence image quality. See also [use previous version](https://github.com/lllyasviel/Fooocus/discussions/1405).

# 2.1.837

* Fix some precision-related problems.

# 2.1.836

* Avoid blip tokenizer download from torch hub

# 2.1.831

* Input Image -> Describe (Midjourney Describe)

# 2.1.830

* SegmindVega support.

# 2.1.829

* Change SDE tree to CPU on AMD/DirectMl to avoid potential problems.

# 2.1.828

* Allow to disable gradio analytics.
* Use html table in log.
* fix some SSL problems.

# 2.1.826

* New backend.
* FP8 support (see also the new cmd flag list in Readme, eg, --unet-in-fp8-e4m3fn and --unet-in-fp8-e5m2).
* Fix some MPS problems.
* GLoRA support.
* Turbo scheduler.

# 2.1.823

(2023 Nov 26) Hi all, the feature updating of Fooocus will be paused for about two or three weeks because we have some other workloads. See you soon and we will come back in mid December. However, you may still see updates if other collaborators are fixing bugs or solving problems.

* Fix some potential problem when LoRAs has clip keys and user want to load those LoRAs to refiners.

# 2.1.822

* New inpaint system (inpaint beta test ends).

# 2.1.821

* New UI for LoRAs.
* Improved preset system: normalized preset keys and file names.
* Improved session system: now multiple users can use one Fooocus at the same time without seeing others' results.
* Improved some computation related to model precision.
* Improved config loading system with user-friendly prints.

# 2.1.820

* support "--disable-image-log" to prevent writing images and logs to hard drive.

# 2.1.819

* Allow disabling preview in dev tools.

# 2.1.818

* Fix preset lora failed to load when the weight is exactly one.

# 2.1.817

* support "--theme dark" and "--theme light".
* added preset files "default" and "lcm", these presets exist but will not create launcher files (will not be exposed to users) to keep entry clean. The "--preset lcm" is equivalent to select "Extreme Speed" in UI, but will likely to make some online service deploying easier.

# 2.1.815

* Multiple loras in preset.

# 2.1.814

* Allow using previous preset of official SAI SDXL by modify the args to '--preset sai'. ~Note that this preset will set inpaint engine back to previous v1 to get same results like before. To change the inpaint engine to v2.6, use the dev tools -> inpaint engine -> v2.6.~ (update: it is not needed now after some tests.)

# 2.1.813

* Allow preset to set default inpaint engine.

# 2.1.812

* Allow preset to set default performance.
* heunpp2 sampler.

# 2.1.810

* Added hints to config_modification_tutorial.txt
* Removed user hacked aspect ratios in I18N english templates, but it will still be read like before.
* fix some style sorting problem again (perhaps should try Gradio 4.0 later).
* Refreshed I18N english templates with more keys.

# 2.1.809

* fix some sorting problem.

# 2.1.808

* Aspect ratios now show aspect ratios.
* Added style search.
* Added style sorting/ordering/favorites.

# 2.1.807

* Click on image to see it in full screen.

# 2.1.806

* Fix some lora problems related to clip.

# 2.1.805

* Responsive UI for small screens.
* Added skip preprocessor in dev tools.

# 2.1.802

* Default inpaint engine changed to v2.6. You can still use inpaint engine v1 in dev tools.
* Fix some VRAM problems.

# 2.1.799

* Added 'Extreme Speed' performance mode (based on LCM). The previous complicated settings are not needed now.

# 2.1.798

* added lcm scheduler - LCM may need to set both sampler and scheduler to "lcm". Other than that, see the description in 2.1.782 logs.

# 2.1.797

* fixed some dependency problems with facexlib and filterpy.

# 2.1.793

* Added many javascripts to improve user experience. Now users with small screen will always see full canvas without needing to scroll.

# 2.1.790

* Face swap (in line with Midjourney InsightFace): Input Image -> Image Prompt -> Advanced -> FaceSwap
* The performance is super high. Use it carefully and never use it in any illegal things!
* This implementation will crop faces for you and you do NOT need to crop faces before feeding images into Fooocus. (If you previously manually crop faces from images for other software, you do not need to do that now in Fooocus.)

# 2.1.788

* Fixed some math problems in previous versions.
* Inpaint engine v2.6 join the beta test of Fooocus inpaint models. Use it in dev tools -> inpaint engine -> v2.6 .

# 2.1.785

* The `user_path_config.txt` is deprecated since 2.1.785. If you are using it right now, please use the new `config.txt` instead. See also the new documentation in the Readme.
* The paths in `user_path_config.txt` will still be loaded in recent versions, but it will be removed soon.
* We use very user-friendly method to automatically transfer your path settings from `user_path_config.txt` to `config.txt` and usually you do not need to do anything.
* The new `config.txt` will never save default values so the default value changes in scripts will not be prevented by old config files.

# 2.1.782

2.1.782 is mainly an update for a new LoRA system that supports both SDXL loras and SD1.5 loras.

Now when you load a lora, the following things will happen:

1. try to load the lora to the base model, if failed (model mismatch), then try to load the lora to refiner.
2. try to load the lora to refiner, if failed (model mismatch) then do nothing.

In this way, Fooocus 2.1.782 can benefit from all models and loras from CivitAI with both SDXL and SD1.5 ecosystem, using the unique Fooocus swap algorithm, to achieve extremely high quality results (although the default setting is already very high quality), especially in some anime use cases, if users really want to play with all these things.

Recently the community also developed LCM loras. Users can use it by setting the sampler as 'LCM', scheduler as 'sgm_uniform' (Update in 2.1.798: scheduler should also be "lcm"), the forced overwrite of sampling step as 4 to 8, and CFG guidance as 1.0, in dev tools. Do not forget to change the LCM lora weight to 1.0 (many people forget this and report failure cases). Also, set refiner to None. If LCM's feedback in the artists community is good (not the feedback in the programmer community of Stable Diffusion), Fooocus may add some other shortcuts in the future.

# 2.1.781

(2023 Oct 26) Hi all, the feature updating of Fooocus will (really, really, this time) be paused for about two or three weeks because we really have some other workloads. Thanks for the passion of you all (and we in fact have kept updating even after last pausing announcement a week ago, because of many great feedbacks)  - see you soon and we will come back in mid November. However, you may still see updates if other collaborators are fixing bugs or solving problems.

* Disable refiner to speed up when new users mistakenly set same model to base and refiner.

# 2.1.779

* Disable image grid by default because many users reports performance issues. For example, https://github.com/lllyasviel/Fooocus/issues/829 and so on. The image grid will cause problem when user hard drive is not super fast, or when user internet connection is not very good (eg, run in remote). The option is moved to dev tools if users want to use it. We will take a look at it later.

# 2.1.776

* Support Ctrl+Up/Down Arrow to change prompt emphasizing weights.

# 2.1.750

* New UI: now you can get each image during generating.

# 2.1.743

* Improved GPT2 by removing some tokens that may corrupt styles.

# 2.1.741

Style Updates:

* "Default (Slightly Cinematic)" as renamed to "Fooocus Cinematic".
* "Default (Slightly Cinematic)" is canceled from default style selections. 
* Added "Fooocus Sharp". This style combines many CivitAI prompts that reduces SDXL blurry and improves sharpness in a relatively natural way.
* Added "Fooocus Enhance". This style mainly use the very popular [default negative prompts from JuggernautXL](https://civitai.com/models/133005) and some other enhancing words. JuggernautXL's negative prompt has been proved to be very effective in many recent image posts on CivitAI to improve JuggernautXL and many other models.
* "Fooocus Sharp" and "Fooocus Enhance" and "Fooocus V2" becomes the new default set of styles.
* Removed the default text in the "negative prompt" input area since it is not necessary now.
* You can reproduce previous results by using "Fooocus Cinematic".
* "Fooocus Sharp" and "Fooocus Enhance" may undergo minor revision in future updates.

# 2.1.739

* Added support for authentication in --share mode (via auth.json).

# 2.1.737

* Allowed customizing resolutions in config. 

Modifying this will make results worse if you do not understand how Positional Encoding works. 

You have been warned.

If you do not know why numbers must be transformed with many Sin and Cos functions (yes, those Trigonometric functions that you learn in junior high school) before they are fed to SDXL, we do not encourage you to change this - you will become a victim of Positional Encoding. You are likely to suffer from an easy-to-fail tool, rather than getting more control.

Your knowledge gained from SD1.5 (for example, resolution numbers divided by 8 or 64 are good enough for UNet) does not work in SDXL. The SDXL uses Positional Encoding. The SD1.5 does not use Positional Encoding. They are completely different. 

Your knowledge gained from other resources (for example, resolutions around 1024 are good enough for SDXL) is wrong. The SDXL uses Positional Encoding. People who say "all resolutions around 1024 are good" do not understand what is Positional Encoding. They are not intentionally misleading. They are just not aware of the fact that SDXL is using Positional Encoding. 

The number 1152 must be exactly 1152, not 1152-1, not 1152+1, not 1152-8, not 1152+8. The number 1152 must be exactly 1152. Just Google what is a Positional Encoding.

Again, if you do not understand how Positional Encoding works, just do not change the resolution numbers.

# 2.1.735

* Fixed many problems related to torch autocast.

# 2.1.733

* Increased allowed random seed range.

# 2.1.728

* Fixed some potential numerical problems since 2.1.723

# 2.1.723

* Improve Fooocus Anime a bit by using better SD1.5 refining formulation.

# 2.1.722

* Now it is possible to translate 100% all texts in the UI.

# 2.1.721

* Added language/en.json to make translation easier.

# 2.1.720

* Added Canvas Zoom to inpaint canvas
* Fixed the problem that image will be cropped in UI when the uploaded image is too wide.

# 2.1.719

* I18N

# 2.1.718

* Corrected handling dash in wildcard names, more wildcards (extended-color).

# 2.1.717

* Corrected displaying multi-line prompts in Private Log.

# 2.1.716

* Added support for nested wildcards, more wildcards (flower, color_flower).

# 2.1.714

* Fixed resolution problems.

# 2.1.712

* Cleaned up Private Log (most users won't need information about raw prompts).

# 2.1.711

* Added more information about prompts in Private Log.
* Made wildcards in negative prompt use different seed.

# 2.1.710

* Added information about wildcards usage in console log.

# 2.1.709

* Allowed changing default values of advanced checkbox and image number.

# 2.1.707

* Updated Gradio to v3.41.2.

# 2.1.703

* Fixed many previous problems related to inpaint.

# 2.1.702

* Corrected reading empty negative prompt from config (it shouldn't turn into None).

# 2.1.701

* Updated FreeU node to v2 (gives less overcooked results).

# 2.1.699

* Disabled smart memory management (solves some memory issues).

# 2.1.698

* Added support for loading model files from subfolders.

# 2.1.696

* Improved wildcards implementation (using same wildcard multiple times will now return different values).

**(2023 Oct 18) Again, the feature updating of Fooocus will be paused for about two or three weeks because we have some other workloads - we will come back in early or mid November. However, you may still see updates if other collaborators are fixing bugs or solving problems.**

# 2.1.695 (requested emergency bug fix)

* Reduced 3.4GB RAM use when swapping base model.
* Reduced 372MB VRAM use in VAE decoding after using control model in image prompt.
* Note that Official ComfyUI (d44a2de) will run out of VRAM when using sdxl and control-lora on 2060 6GB that does not support float16 at resolution 1024. Fooocus 2.1.695 succeeded in outputting images without OOM using exactly same devices.

(2023 Oct 17) Announcement of update being paused.

# 2.1.693

* Putting custom styles before pre-defined styles.
* Avoided the consusion between Fooocus Anime preset and Fooocus Anime style (Fooocus Anime style is renamed to Fooocus Masterpiece because it does not make images Anime-looking if not using with Fooocus Anime preset).
* Fixed some minor bugs in Fooocus Anime preset's prompt emphasizing of commas.
* Supported and documented embedding grammar (and wildcards grammar). 
* This release is a relative stable version and many features are determined now.

# 2.1.687

* Added support for wildcards (using files from wildcards folder - try prompts like `__color__ sports car` with different seeds).

# 2.1.682

* Added support for custom styles (loaded from JSON files placed in sdxl_styles folder).

# 2.1.681

* Added support for generate hotkey (CTRL+ENTER).
* Added support for generate forever (RMB on Generate button).
* Added support for playing sound when generation is finished ('notification.ogg' or 'notification.mp3').

# 2.1.62

* Preset system. Added anime and realistic support.

# 2.1.52

* removed pygit2 dependency (expect auto update) so that people will never have permission denied problems.

# 2.1.50

* Begin to support sd1.5 as refiner. This method scale sigmas given SD15/Xl latent scale and is probably the most correct way to do it. I am going to write a discussion soon.

# 2.1.25

AMD support on Linux and Windows.

# 2.1.0

* Image Prompt
* Finished the "Moving from Midjourney" Table

# 2.0.85

* Speed Up Again

# 2.0.80

* Improved the scheduling of ADM guidance and CFG mimicking for better visual quality in high frequency domain and small objects.

# 2.0.80

* Rework many patches and some UI details.
* Speed up processing.
* Move Colab to independent branch.
* Implemented CFG Scale and TSNR correction when CFG is bigger than 10.
* Implemented Developer Mode with more options to debug.

### 2.0.72

(2023 sep 21) The feature updating of Fooocus will be paused for about two or three weeks because we have some events and travelling - we will come back in early or mid October. 

### 2.0.72

* Allow users to choose path of models.

### 2.0.65

* Inpaint model released.

### 2.0.50

* Variation/Upscale (Midjourney Toolbar) implemented.

### 2.0.16

* Virtual memory system implemented. Now Colab can run both base model and refiner model with 7.8GB RAM + 5.3GB VRAM, and it never crashes.
* If you are lucky enough to read this line, keep in mind that ComfyUI cannot do this. This is very reasonable that Fooocus is more optimized because it only need to handle a fixed pipeline, but ComfyUI need to consider arbitrary pipelines. 
* But if we just consider the optimization of this fixed workload, after 2.0.16, Fooocus has become the most optimized SDXL app, outperforming ComfyUI.

### 2.0.0

* V2 released.
* completely rewrite text processing pipeline (higher image quality and prompt understanding).
* support multi-style.
* In 100 tests (prompts written by ChatGPT), V2 default results outperform V1 default results in 87 cases, evaluated by two human.
* In 100 tests (prompts written by ChatGPT), V2 prompt understanding outperform V1 prompt understanding in 81 cases, evaluated by two human, in both default setting and multi/single style mode.
* Because the above number is above 80%, we view this as a major update and directly jump to 2.0.0.
* Some other things are renamed.

### 1.0.67

* Use dynamic weighting and lower weights for prompt expansion.

### 1.0.64

* Fixed a small OOM problem.

### 1.0.62

* Change prompt expansion to suffix mode for better balance of semantic and style (and debugging).

### 1.0.60

* Tune the balance between style and Prompt Expansion.

### 1.0.56

* Begin to use magic split.

### 1.0.55

* Minor changes of Prompt Expansion.

### 1.0.52

* Reduce the semantic corruption of Prompt Expansion.

### 1.0.51

* Speed up Prompt Expansion a bit.

### 1.0.50

* Prompt expansion and a "Raw mode" to turn it off (similar to Midjourney's "raw").

### 1.0.45

# RuinedFooocus Update Logs

### 1.55.0
* Pixart and Flux oh my!

### 1.53.0
* MergeMaker

### 1.52.0
* Merge-recipes for checkpoints

### 1.51.0
* Bugfixes
* Now works with the SD3 LARGE model.
* OBP Update!!!

### 1.50.0
* SD3 BBY

### 1.40.1
* Support animated thumbnails

### 1.40.0
* New LoRA selection
* Updated OBP

### 1.39.0
* New model selection with model previews!


### 1.38.1
* Minor Fixes

### 1.38.0
* Added HyperPrompt to styles / OBP
* Added handy hints!

### 1.37.1
* Fixed missing clip skip in some performances

### 1.37.0
* Updated Comfy Version
* Tidied Code
* Added CLipSkip

### 1.36.0
* Added search pipeline, Type "search:" in prompt to get todays images

### 1.35.0
* Added LayerDiffuse to create transparent images with an optional background image  `Powerup Tab`
* Artify Update: NMake sure you check the style selection for a TON of new styles to try
* OBP Update

### 1.34.0
* Added llyasviel's prompt tokenizer model for improving prompts, This can be used by adding the `Flufferizer` style

### 1.33.1
* Moved upscale to its own pipeline
* Various Bug Fixes

### 1.33.0
* Updated to latest comfy version
* Now supports Playground 2.5 model!

### 1.32.0
* Various Bugfixes
* Adds the ability to upgrade to a newer torch and xformers, just create a blank `reinstall` file in the RF directory

### 1.31.0
* Added presets / custom preset for OBP
* Various Bugfixes

### 1.30.0
* The OBP Update
* added "the tokinator" mode
* Fintetunes on autonegative prompt: -- Landscape removed
* Added list of artist shorthands (like van gogh)
* Added secret sauce mode (mixing OBP + SDXL styles). Happens more on lower insanity levels
* Added more consistency on lower insanity levels
* EVO with OPB variant works better:
* Small prompts now work
* (almost) always changes something
* Fix for line ends creeping into EVO + OPB Variant
* Added loads of new styles into the lists
* Added loads of more fictional characters into the lists (finally, harley quinn is in :p)

### 1.29.0
* Automatic Negative prompt, save yourself the heartache and hassle of writing negative prompts!

### 1.28.2
* Fixed some dodgy regex to support wildcards with `-` in the name

### 1.28.1
* Added better error descriptions for the civit api

### 1.28.0
* Automatically grabs lora keywords from civit on startup

### 1.27.0
* Advance prompt editing - See [Wiki](https://github.com/runew0lf/RuinedFooocus/wiki/Features#advanced-prompt-editing)
* Moved Evolve to the `Powerup` tab to be cleaner
* Bufixes

### 1.26.1
* Changed so loras with triggerwords textfiles dont automatically get added, instead displays trigger words to add manually

### 1.26.0
* Fixed issue with controlnet caching
* Custom resolutions can now be saved directly, just select custom from the resolution dropdown (Lavorther)
* re-enabled comfy messages

### 1.25.5
* Make Custom option for Performance Mode copy last selected mode's setings (Lavorther)

### 1.25.4
* Fixed an issue with wildcards and strengths getting stuck in Catastrophic backtracking

### 1.25.3
* Changed a lot of os.path to pathlibs
* Worked on backend code for future extensibility
* Added support for --auth

### 1.25.2
* Fixed an os.path issue by replaceing with pathlib

### 1.25.1
* Now displays 🗒️ at the end of the loraname if it has a keyword .txt file

### 1.25.0
* Prompt Bracketing Now works ie `[cat|dog]`
* Updated comfy version

### 1.24.2
* More Tidying and tweaks
* Autoselect LCM lora if Lcm is selected from the quality or sampler dropdowns

### 1.24.1
* Code Tidying and tweaks

### 1.24.0
* Added Evolve which generates variations on your generated picture.
* Fixed wild imports
* Added instant One Button Prompt
* Added keybind of `ctrl+shift` to toggle `hurt me plenty`` mode
* Code Cleanup
* Fixed Issue with dropdown box's being case sensitive when sorting

### 1.23.2
* Adds token count (thanks Lavorther)
* Fixed lora keywords only working the first time the lora is loaded

### 1.23.1
* Use OneButtonPrompt with infinite mode, simply put a tick in `BYPASS SAFETY PROTOCOLS`

### 1.23.0
* Inpainting Update: Adds inpainting to the powerup tab

### 1.22.0
* Now comes with a built in clip interrogator, just drag your image onto the main image to generate the prompt

### 1.21.0
* Π Time - Click the small Π symbol to get a fullscreen image of your last generation great for slideshows
* updated comfy version, NEW SAMPLER TIME

### 1.20.0
* Added wildcard helper, just start typing __ and your wildcards will display
* Added slideshow

### 1.19.5
* Fixed old bug of switching models when the stop button is pressed (old code from OG-F)

### 1.19.4
* Old experimental lcm-pipeline removed
* Generate forever if Image Number is set to 0
* Updated comfy version to latest
* Nested wildcards now supported

### 1.19.3
* Random styles now correctly applying to each image

### 1.19.2
* Gradio Rollback to v3 until v4 is fixed

### 1.19.1
* WildCard Fixes
* Automatcially downloads LCM Models
* Now checks subdirectories for models

### 1.19.0
* Gradio update to V4

### 1.18.0
* New Random Style Selection
* Adding one button prompt overrides in wildcards now
* Added wildcards official
* Other stuff i'll have to get arljen to explain

### 1.17.2
* Limit seeds to 32 bits
* Sort model dropdowns
* Use caches better

### 1.17.1
* removed groop and faceswap as it was causing dependency issues on some systems

### 1.17.0
* Changed minimum cfg scale to 0
* Updated to latest comfy and diffusers (Now supports LCM Loras)
* You NEEED to set the custom settings to use lcm and sgm_sampler, steps of 4 and REALLY low config (between 0 and 1.5)

### 1.16.0
* Facewapping
* Groop

### 1.15.1
* Updated Comfy Version

### 1.15.0
* Different pipelines supporting lcm and sdxl/ssd
* Let async_worker handle model preload
* Lots of small fixes
* fixed metadata bug when stopped

### 1.14.1
* Fixed small issue with metadata not updating

### 1.14.0
* Added Metadata Viewer for Gallery items (Viewable in `Info` Tab)
* Refresh Files now also reloads your `styles.csv` file

### 1.13.0
* Automatically download 4xUltrasharp Upscaler
* Added the ability to upscale images wth upscaler of your choosing
* Changed Powerup Settings so if there is a missing key from defaults it adds it to your custome settings.

### 1.12.1
* Refactored backend code to allow for future pipeline changes

### 1.12.0
* Automatically read triggerwords from <lora_filename>.txt

### 1.11.0
* Updated Comfy Version
* Added support for [SSD-1B Models](https://huggingface.co/segmind/SSD-1B)

### 1.9.0
* Removed ref redundant code.

### 1.8.2
* Update Comfy version and fix changes :D

### 1.8.1
* Improved image2image and allowed settings to be changed when "custom" is selected form the PowerUp Tab.

### 1.8.0
* Added the basics for image 2 image
* Renamed Controlnet to PowerUp
* Now uses `powerup.json` as default

### 1.7.2
* Wildcards can now use subdirectories
* Fixed issue where if you placed 2 placeholders with the same name, you got the same results, a new one is now chosen
* Updated status to show model loading / vae decoding

### 1.7.1
* Update to one button prompt (provided by [Alrjen](https://github.com/AIrjen/OneButtonPrompt))

### 1.7.0
* Custom Controlnet Modes
* minor bugfixes
* moved the controlnet tab to its own ui file.

### 1.6.1
* Added sketch controlnet!

### 1.6.0
* Updated gradio version
* Added recolour controlnet!

### 1.5.2
* Restored gallery preview on all images
* renamed more variables to make sense
* bugfixes

### 1.5.1
* Added all the settings/customization to their own `settings` folder **NOTE:** you will need to move / copy your settings into the new directory
* Bugfix where clicking stop mid-generation stopped working
* code cleanup and some renaming
* inference model speed up
* now only shows gallery when needed

### 1.5.0
* removed metadata toggle, it will now always save metadata
* save your own custom performances
* tidied ui
* fix crash when failing to load loras
* hide all but one lora dropdown showing "None"

### 1.4.2
* change fooocusversion.py to version.py for easier updating
* Moved controlnet to its own tab for easier updates
* updated gradio version
* minor wording changes

### 1.4.1
* `paths.json` will now be updated if there are any missing defaults paths

### 1.4.0
* Now supports controlnet

### 1.3.0
* Updated onebutton prompt so you can now add multiple random prompts by clicking the `Add To Prompt` button

### 1.2.2
* Update comfy version - Lora weights are now calculated on the gpu so should apply faster
### 1.2.1
* Bug fixes and backend updates
* changed `resolutions.csv` to `resolutions.json`
* updated readme

### 1.2.0
* Prompt now splits correctly using `---`
* added the ability to change styles in the prompt by using <style:stylename>

### 1.1.7
* Added init image

### 1.1.6
* Fixed issue with wildcards if file not found.

### 1.1.5
* Fixed sorting on subfolders, so directories are displayed first

### 1.1.4
* Allowed main image window to recieve drag and drop
* Added a gallery preview underneath that will activate image window.

### 1.1.3
* Added support for subdirectories with models/loras so you can get all organised!

### 1.1.2
* showed imported image in gallery 
* moved `---` split into prompt generation
* correctly updates progressbar
* fixed importing of width / height

### 1.1.1
*  In the json prompt, setting a seed of `-1` allows you to generate a random seed

### 1.1.0
*  Render different subjects so you can process a whole list of prompts. Seperate each prompt by placing `---` on a new line

### 1.0.0
* New Beginnings. The official start of the updates!
