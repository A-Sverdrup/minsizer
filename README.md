# minsizer
Automatically compress JPEG/JFIF, PNG*, BMP, GIF and TIFF** images into WebP or AVIF using cwebp, gif2webp, avifenc, cavif, tiff2png and  bmp2png.
```
minsizer4
minsizer4 /?
minsizer4 [-h/--help]
minsizer4 [/MODE <mode>] [/E] [/Q] [dir/input1] [input2...inputN]
minsizer4 [-m/--mode <mode>] [-e] [-q] [dir/input1] [input2...inputN]
--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG*, BMP, GIF and TIFF** images into WebP or
AVIF using cwebp, gif2webp, avifenc, cavif, tiff2png and  bmp2png.

*  Caution: APNG animation will not be preserved!
** Caution: Alpha-channel will not be preserved!

Only the smallest resulting file is kept. If the original (unconverted) file was
kept as smallest, it will not be converted next run (skipped).

Almost in-place conversion. Requires at most 4x as much space as the largest
image (by file size, not image dimensions) in the set

Conversion time depends mostly on your hardware and can easily reach multiple
hours when converting large (thousands of pictures) datasets. JPG is faster to
convert, PNG is slower  and BMP and TIFF are slowest.

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
