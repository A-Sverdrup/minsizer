# minsizer
Automatically compress JPEG/JFIF, PNG*, BMP**, GIF*** and TIFF*** images into WebP or AVIF using cwebp and gif2webp (https://chromium.googlesource.com/webm/libwebp), avifenc (https://github.com/AOMediaCodec/libavif), cavif (https://github.com/link-u/cavif), tiff2png and bmp2png (https://libpng.org/) and magick (https://imagemagick.org/).

(cwebp, gif2webp, avifenc, cavif, tiff2png, bmp2png and magick) ARE provided with release packages.

```
minsizer5
minsizer5 /?
minsizer5 [-h/--help]
minsizer5 [/MODE <mode>] [/A] [/E] [/Q] [input1] [input2...inputN]
minsizer5 [-m/--mode <mode>] [-a] [-e] [-q] [input1] [input2...inputN]
--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG, BMP, GIF and TIFF images into WebP or
AVIF using cwebp, gif2webp, avifenc, cavif, tiff2png, bmp2png and ImageMagick
with the highest quality possible (lossless or lossy >99%) and highest posible
compression effort.

Can also try and recompress WebP using ImageMagick.

Important notices:

PNG:
Unavoidable data loss: APNG is unsupported. APNG animation will be LOST!
Data loss warning:     Alpha-channel is not preserved by default and will be
                       LOST!
Inefficiency:          When preserving alpha-channel, cavif is disabled as it
                       does not support transparency. avifenc is used instead,
                       but it has worse compression ratio.
Compatibility issue:   AVIF files produced by cavif can be incorrectly reported
                       as "corrupted" by Mozilla Firefox and Safari.
BMP:
Data loss warning: If a PNG file with the same name is present in the same
                   folder, it will be LOST. This is an oversight caused by
                   bmp2png and cannot be easily fixed.
GIF:
Data loss warning:   gif2webp is not entirely lossless.
Compatibility issue: Most software do not support animated WebP.

TIFF:
Data loss warning: Alpha-channel is not preserved by default and will be LOST!
Inefficiency:      When preserving alpha-channel, cavif is disabled as it does
                   not support transparency. avifenc is used instead, but it has
                   worse compression ratio.
Data loss warning: If a PNG file with the same name is present in the same
                   folder, it will be LOST. This is an oversight caused by
                   tiff2png and cannot be easily fixed.

Only the smallest resulting file is kept. If the original (unconverted) file was
kept as smallest, it will not be converted next run (skipped).

Almost in-place conversion. Requires at most 6x (BMP/TIFF) / 5x (PNG) / 4x (JPG) / 3x (GIF)
as much disk space as the largest image by file size in the dataset.

Conversion time depends mostly on your hardware and can easily reach multiple
hours and even days when converting large datasets (thousands of pictures).
JPG is faster to convert, PNG is slower and BMP and TIFF are slowest.

Does not accept arguments to pass-through to codecs! Edit source code to see
defaults and tweak codec parameters. See cwebp, gif2webp, avifenc, cavif, 
bmp2png and tiff2png manpages to understand parameters.

Dependencies (cwebp.exe, gif2webp.exe, avifenc.exe, cavif.exe, bmp2png.exe,
tiff2png.exe, magick.exe) are expected to be found in ./lib subfolder or on PATH

minsizer5: Convert images in current folder and all its subfolders in 
           interactive mode
           
minsizer5 [-m/--mode] OR minsizer5 /MODE: Automatic mode: specify filetypes
                                          J/P/B/G/T/*:
                                          J: JPEG/JFIF only
                                          P: PNG only
                                          B: BMP only
                                          G: GIF only
                                          T: TIFF only
                                          W: WebP only
                                          A: AVIF only (does nothing)
                                          *: Everything except GIF and WEBP
                                          (equivalent to 'JPBT')
                                          
                                          Combinations of above symbols may also
                                          be used, e.g. 'JP' will convert both
                                          JPG and PNG images, 'BPT' will
                                          convert BMP, PNG and TIFF images and
                                          '*GW' will convert every supported
                                          image type
                                          
minsizer5 [-a] OR minsizer5 /A: Preserve alpha-channel for PNG and TIFF.

minsizer5 [-e] OR minsizer5 /E: Ignore errors and proceed, do not ask user input
                                to continue.
                                
minsizer5 [-q] OR minsizer5 /Q: Quit after finishing conversion, do not ask user
                                input to exit.

minsizer5 [-h/--help] OR minsizer5 /?: Show this help message and exit.

minsizer5 input1 [input2] ... [inputN]: If input is an image, convert the input
                                        image.
                                        If input is a folder, convert all images
                                        in input folder and all its subfolders. 

minsizer5 dir: Converts all images in <dir> and all its subfolders. 
minsizer5 input: Convert a single image. Sets /MODE to '*' and enables /E
'''
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

minsizer3.1: unknown whether it even existed

minsizer3.2: initial bmp2png support

minsizer3.4: switch from os.system to subprocess.Popen as backend, make 2-step conversion ( X -> png -> avif/webp) modular, make sample image-based binary testing modular

minsizer3.5: minor tweaks, python-embedded-package compatibility

## minsizer4

minsizer4: Total UI overhaul. Interactive mode. Proper command-line arguments. Documentation and help-string.

minsizer4.2: Improve UI (more responsive, but still not real-time). Initial Ctrl+C SIGTERM handling.

minsizer4.3: Add option to preserve alpha-channel. Modify UI

## minsizer5

minsizer5: Redo UI (still not real-time).

minsizer5.2: Initial magick support

## Future versions

TODO: Fix skip list being broken since 3.0

minsizer6: Total UI overhaul (real-time progress monitoring).

minsizer7: The final version..?



