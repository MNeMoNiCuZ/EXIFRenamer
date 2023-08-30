# EXIFRenamer
Python script to rename files based to EXIF data

Currently only reads .PNG-files.

Drag/drop files or folders onto the script.
Alternatively you can run the script and it will ask you for a file path.

Once it detects at least 1 image, it will try to locate EXIF metadata from this list: [Positive, Negative, Steps, Sampler, CFG scale, Seed, Size, Model, Denoising strength, Clip skip, Hires upscale, Hires steps, Hires upscaler, Lora hashes].

The user then gets to choose which data to add to the file name, and if it should be added as a prefix or suffix.

In the settings.ini-file you can choose how to separate the original name from the new prefix/suffix, and if it should keep the original name at all.
