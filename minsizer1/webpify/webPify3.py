from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
'''
Automatically compress images in current folder and all its subfolders into WebP.
Default (see source code):
JPG JPEG -> lossy, 100% quality, noalpha
PNG BMP -> lossless, noalpha
See cwebp manpage for more details on cwebp parameters

Almost in-place conversion. Requires as much space as the biggest image (or a bit more).
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
    fl={i:(i+'.webp')for i in incepts([getcwd()+sep],ext)}
    for i in fl:
        r=system('%s -quiet %s "%s" -o "%s"'%(binary,params,i,fl[i]))
        if r:print('cwebp fail',i)
        else:
            try:
                if getsize(fl[i])<getsize(i):remove(i);print('replace %s -> %s'%(i,fl[i]))
                else:remove(fl[i]);print('keep',i)
            except:print('fail',i)
for i in formats:convert(i,formats[i])
input('\nAll done! Press enter to exit.')
exit()


