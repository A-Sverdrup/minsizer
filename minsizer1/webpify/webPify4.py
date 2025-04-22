from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
from pickle import dump,load
'''
Automatically compress images in current folder and all its subfolders into WebP.
See source code for default parameters. Read cwebp manpage to understand.

Almost in-place conversion. Requires as much space as the biggest image (or a bit more).
If resulting WebP is larger than original picture, the original is kept instead.

Full cross-platform! On android run "pkg install libwebp" in Termux first.
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
try:
    with open('skip.pickle','rb')as f:skip=load(f);print('skipping files:',*skip,sep='\n')
except:skip=set()
skip2=set()
def incepts(a,b):return sum([sorted(sum([glob(i+j)for j in b],[]))+incepts(sorted(glob(i+'*'+sep)),b)for i in a],[])
def convert(ext,params):
    fl={i:(i+'.webp')for i in list(set(incepts([getcwd()+sep],ext))-skip)}
    for i in fl:
        r=system('%s -quiet %s "%s" -o "%s"'%(binary,params,i,fl[i]))
        if r:print('cwebp fail',i)
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


