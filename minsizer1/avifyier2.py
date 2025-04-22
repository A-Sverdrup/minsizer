from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
from pickle import dump,load
'''
Automatically compress images in current folder and all its subfolders into avif.
See source code for default parameters. Read avifenc manpage to understand.

Almost in-place conversion. Requires as much space as the biggest image (or a bit more).
If resulting AVIF is larger than original picture, the original is kept instead.

Cannot be used on android because no libavif on Termux.
Dependencies: avifenc binary on PATH or in current directory
'''
binary='.%savifenc'%sep
with open('amihere.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
if system(binary +' amihere.png amihere.avif'):
    binary='avifenc'
    if system(binary +' amihere.png amihere.avif'):
        print('avifenc not found!',file=__import__('sys').stderr);exit();
files={}
formats={('*.jpg','*.jpeg'):'--qalpha 0 -d 8',
         ('*.png','*.bmp'):'-q 100 -d 8',
         }
try:
    with open('skip.pickle','rb')as f:skip=load(f);print('skipping files:',*skip,sep='\n')
except:skip=set()
skip2=set()
def incepts(a,b):return sum([sorted(sum([glob(i+j)for j in b],[]))+incepts(sorted(glob(i+'*'+sep)),b)for i in a],[])
def convert(ext,params):
    fl={i:(i+'.avif')for i in list(set(incepts([getcwd()+sep],ext))-skip)}
    for i in fl:
        r=system('%s %s "%s" -o "%s"'%(binary,params,i,fl[i]))
        if r:print('avifenc fail',i)
        else:
            try:
                if getsize(fl[i])<getsize(i):remove(i);print('replace %s -> %s'%(i,fl[i]))
                else:remove(fl[i]);print('keep',i);skip2.add(i)
            except:print('fail',i)
for i in formats:convert(i,formats[i])
skip.update(skip2)
try:
    with open('skip.pickle','wb')as f:dump(skip,f);print('saved skip list')
except:print('fail saving skip list')
input('\nAll done! Press enter to exit.')
exit()


