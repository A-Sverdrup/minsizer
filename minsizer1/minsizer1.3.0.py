from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
from math import nan;from sys import platform
from pickle import dump,load
'''
Automatically compress images in current folder and all its subfolders into WebP or AVIF using cwebp, avifenc and cavif.
See source code for default parameters
See cwebp, avifenc and cavif manpages to understand parameters

Almost in-place conversion. Requires 3-3.5x as much space as the largest image.
Only the smallest file (original/WebP/AVIF/AVIF) is kept.

Windows only because AVIF implementations are a mess!
Dependencies: cwebp.exe, avifenc.exe and cavif.exe binary on PATH or in current directory
'''
nil='nul'if platform=='win32'else'/dev/null'
cwebp='.%scwebp'%sep
if system(cwebp+' > '+nil):
    webp='cwebp'
    if system(cwebp+' > '+nil):
        print('cwebp not found!',file=__import__('sys').stderr);exit();
cavif='.%scavif'%sep
with open('amihere.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
if system(cavif +' -i amihere.png -o amihere.avif > '+nil):
    cavif='cavif'
    if system(cavif +' -i amihere.png -o amihere.avif > '+nil):
        print('cavif not found!',file=__import__('sys').stderr);exit();
try:remove('amihere.png')
except:print('cannot remove test file!')
try:remove('amihere.avif')
except:print('cannot remove test file!')
avifenc='.%savifenc'%sep
with open('amihere.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
if system(avifenc +' amihere.png amihere.avif > '+nil):
    avifenc='avifenc'
    if system(avifenc +' amihere.png amihere.avif > '+nil):
        print('avifenc not found!',file=__import__('sys').stderr);exit();
try:remove('amihere.png')
except:print('cannot remove test file!')
try:remove('amihere.avif')
except:print('cannot remove test file!')
files={}
formats={('*.jpg','*.jpeg'):
          {avifenc:'--qalpha 0 -d 8',
           cwebp:'-quiet -q 100 -noalpha'},
      ('*.png',):
          {cavif:'--lossless -i',
           avifenc:'-q 100 --qalpha 0 -d 8',
           cwebp:'-quiet -noalpha -lossless'},
      ('*.bmp',):
          {avifenc:'-q 100 --qalpha 0 -d 8',
           cwebp:'-quiet -noalpha -lossless'},
     }
exts={avifenc:'.avif',cwebp:'.webp',cavif:'.c.avif'}
try:
    with open('skip.pickle','rb')as f:skip=load(f);print('skipping files:',*skip,sep='\n')
except:skip=set()
skip2=set()
def incepts(a,b):return sum([sorted(sum([glob(i+j)for j in b],[]))+incepts(sorted(glob(i+'*'+sep)),b)for i in a],[])
def cmd(*a):return system('%s %s "%s" -o "%s" > %s'%(*a,nil))
def getsizenan(path):
    try:return getsize(path)
    except:return nan
def convert(ext):
    print(f:=list(set(incepts([getcwd()+sep],ext))-skip))
    for i in f:
        fl={i:getsizenan(i)}
        for j in formats[ext]:
            print(j)
            cmd(j,formats[ext][j],i,(w:=i+exts[j]))
            fl[w]=getsizenan(w)
        print('\n\n',fl,'\n\n')
        m=min(fl,key=lambda i:fl[i])
        fl.pop(m)
        if m==i:skip2.add(i);print('keep',i)
        else:print('minsized',m)
        for j in fl:
            try:remove(j)
            except:print('fail deleting %s!'%j)
for i in formats:convert(i)
skip.update(skip2)
try:
    with open('skip.pickle','wb')as f:dump(skip,f);print('saved skip list')
except:print('fail saving skip list')
input('\nAll done! Press enter to exit.')
exit()


