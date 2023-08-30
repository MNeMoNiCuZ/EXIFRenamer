# EXIFRenamer
This is a Python script to rename files based to EXIF data.
Currently only reads .PNG-files.

The intention is to use this to batch-rename images generated with Stable Diffusion (Automatic 1111), based on the data you need.
Example: Maybe you want to at a glance see which files are generated with which sampling method, or checkpoint model.

# How to use
Drag/drop files or folders onto the script.
Alternatively you can run the script and it will ask you for a file path.

If it detects at least 1 image, it will try to find some EXIF metadata from this list: [Positive, Negative, Steps, Sampler, CFG scale, Seed, Size, Model, Denoising strength, Clip skip, Hires upscale, Hires steps, Hires upscaler, Lora hashes].

The user then chooses which data to add to the file name, and if it should be added as a prefix or suffix.

In the settings.ini-file you can choose how to separate the original name from the new prefix/suffix, and if it should keep the original name at all.

The included EXIFRenamer.bat-file can be used to run or drag/drop the files to, instead of the EXIFRenamer.py, this one should keep the window open if you run into some errors.

![Demo](https://github.com/MNeMoNiCuZ/EXIFRenamer/assets/60541708/35560636-3418-481e-955c-65ed729f1f59)
