# minsizer
Automatically compress JPEG/JFIF, PNG*, BMP, GIF and TIFF** images into WebP or AVIF using cwebp, gif2webp, avifenc, cavif, tiff2png and  bmp2png.
```
minsizer4
minsizer4 /?
minsizer4 [-h/--help]
minsizer4 [/MODE <mode>] [/E] [/Q] [dir/input1] [input2...inputN]
minsizer4 [-m/--mode <mode>] [-e] [-q] [dir/input1] [input2...inputN]
--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG, BMP, GIF and TIFF images into
WebP or AVIF using cwebp, gif2webp, avifenc, cavif, tiff2png and  bmp2png.

Important notices:

PNG:
Unavoidable data loss: APNG is unsupported. APNG animation will be LOST!
Data loss warning:     Alpha-channel is not preserved by default and will be
                       LOST!
Compatibility issue:   AVIF files produced by cavif are incorrectly reported as
                       "corrupted" by Mozilla Firefox and Safari
BMP:
Data loss warning: If a PNG file with the same name is present in thesame folder,
                   it will be LOST. This is an oversight caused by bmp2png and
                   cannot be easily fixed.
GIF:
Compatibility issue: Most software do not support animated WebP.

TIFF:
Data loss warning: Alpha-channel is not preserved by default and will be LOST!
Data loss warning: If a PNG file with the same name is present in thesame folder,
                   it will be LOST. This is an oversight caused by tiff2png and
                   cannot be easily fixed.

Only the smallest resulting file is kept. If the original (unconverted) file was
kept as smallest, it will not be converted next run (skipped).

Almost in-place conversion. Requires at most 4x as much disk space as the
largest image by file size in the dataset.

Conversion time depends mostly on your hardware and can easily reach multiple
hours and even days when converting large datasets (thousands of pictures).
JPG is faster to convert, PNG is slower and BMP and TIFF are slowest.

Does not accept arguments to pass-through to codecs! Edit source code to see
defaults and tweak codec parameters. See cwebp, gif2webp, avifenc, cavif and
tiff2png manpages to understand parameters.

Dependencies (cwebp.exe, gif2webp.exe, avifenc.exe, cavif.exe, bmpp2png.exe,
tiff2png.exe) are expected to be found in ./lib subfolder or on PATH

minsizer4: Convert images in current folder and all its subfolders in
           interactive mode

minsizer4 [-m/--mode] OR minsizer4 /MODE: Automatic mode: specify filetypes
                                          J/P/B/G/T/*:
                                          J: JPEG/JFIF only
                                          P: PNG only
                                          B: BMP only
                                          G: GIF only
                                          T: TIFF only
                                          *: Everything  except GIF (equivalent
                                          to 'JPBT')
                                          Combinations of above symbols may also
                                          be used, e.g. 'JP' will convert both
                                          JPG and PNG images and 'GT' will
                                          convert GIF and TIFF images
minsizer4 [-a] OR minsizer4 /A: Preserve alpha-channel for PNG and TIFF.

minsizer4 [-e] OR minsizer4 /E: Ignore errors and proceed, do not ask user input
                                to continue.

minsizer4 [-q] OR minsizer4 /Q: Quit after finishing conversion, do not ask user
                                input to exit.

minsizer4 [-h/--help] OR minsizer3 /?: Show this help message and exit.

minsizer4 input1 [input2] ... [inputN]: If input is an image, convert the input
                                        image.
                                        If input is a folder, convert all images
                                        in input folder and all its subfolders.

minsizer4 dir: Converts all images in <dir> and all its subfolders.
minsizer4 input: Convert a single image. Sets /MODE to '*' and enables /E
```

# changelog

## minsizer1
webpify and avifyier (all  versions): shitty little scripts to automatically convert images in current folder into webp only and avif only respectively

minsizer1: merge webpify and avifyier

minsizer1.2: fix args, quiet mode

minsizer1.3.0: initial cavif support

minsizer1.3.5: initial documentation, refactoring

minsizer1.4: improve ui (add statistics), initial gif2webp support

minsizer1.5: add dry-run

## minsizer2

minsizer2: lost media. unknown.

minsizer2.1: initial tiff2png support, improve statistics

minsizer2.2: documentation, refactoring (modular system)

## minsizer3

minsizer3.0: switch from incepts to globator, improve ui (add Images Found), improve modular system, documentation, accept commandline argument as input, python-embedded-package compatibility

minsizer3.2: initial bmp2png support

minsizer3.4: switch from os.system to subprocess.Popen as backend, make 2-step conversion ( X -> png -> avif/webp) modular, make sample image-based binary testing modular

minsizer3.5: minor tweaks, python-embedded-package compatibility

## minsizer4

minsizer4: Total UI overhaul. Interactive mode. Proper command-line arguments. Documentation and help-string.

minsizer4.5: Improve UI (more responsive, but still not real-time). Initial Ctrl+C SIGTERM handling.

## minsizer5

Snooping as usual, i see? These are FUTURE versions.

minsizer5: Add option to preserve alpha-channel. Modify UI

minsizer5.5: Redo UI (still not real-time).

minsizer6: Total UI overhaul (real-time progress monitoring).

minsizer6.5: Initial ffmpeg support.

minsizer7: The final version..?



