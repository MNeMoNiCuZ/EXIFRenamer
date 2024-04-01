# EXIFRenamer
EXIFRenamer is a Python script designed for batch renaming image files based on their EXIF metadata. At present, the script supports only .PNG files. It is particularly useful for organizing images generated with Stable Diffusion (Automatic 1111) by incorporating relevant EXIF data directly into the file names. This functionality allows for quick identification of images based on various parameters such as sampling method, checkpoint model, and more, without the need to view the file's metadata.

# How to Use
To rename files using EXIFRenamer, you can either drag and drop files or folders onto the script or run the script through a command-line interface, where it will prompt you to enter a file path. Upon detecting at least one image, the script scans for EXIF metadata including, but not limited to, Positive, Negative, Steps, Sampler, CFG scale, Seed, Size, Model, Denoising strength, Clip skip, Hires upscale, Hires steps, Hires upscaler, and Lora hashes.

Users are given the option to select which metadata fields to incorporate into the file name and to specify whether this information should be added as a prefix or a suffix.

Configuration options, such as how to delimiter the original name from the added prefix/suffix and whether to retain the original name, can be adjusted in the `settings.ini` file.

For ease of use, an `EXIFRenamer.bat` file is included. This batch file can be executed directly or used as a drag-and-drop target for files and folders. It is designed to keep the command window open, which is helpful for troubleshooting any errors encountered during the renaming process.

![Demo](https://github.com/MNeMoNiCuZ/EXIFRenamer/assets/60541708/35560636-3418-481e-955c-65ed729f1f59)
