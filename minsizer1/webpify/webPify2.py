from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
'''
Automatically compress images in current folder and all its subfolders into WebP.
Default (see source code):
JPG JPEG -> lossy, 100% quality, noalpha
PNG BMP -> lossless, noalpha
See cwebp manpage for more details on cwebp parameters

Not in-place conversion! Requires at least as much free disk space as original images.
If resulting WebP is larger than original picture, the original is kept instead.

Dependencies: cwebp binary on PATH or in current dirrectory
'''
binary='.%scwebp'%sep
if system(binary):
    binary='cwebp'
    if system(binary):
        print('cwebp not found!',file=__import__('sys').stderr);exit();
files={}
formats={('*.jpg','*.jpeg'):'-q 100 -noalpha',
         ('*.png','*.bmp'):'-noalpha -lossless',
         }
def incepts(a,b):return sum([sorted(sum([glob(i+j)for j in b],[]))+incepts(sorted(glob(i+'*'+sep)),b)for i in a],[])
def convert(ext,params):
    fl={i:(i+'.webp')for i in incepts([getcwd()],ext)}
    for i in fl:system('%s %s "%s" -o "%s"'%(binary,params,i,fl[i]))
    files.update(fl)
for i in formats:convert(i,formats[i])
for i in files:
    try:
        if getsize(files[i])<getsize(i):remove(i);print('replace',files[i])
        else:remove(files[i]);print('keep',i)
    except:print('fail',i)
input('\nAll done! Press enter to exit.')
exit()


