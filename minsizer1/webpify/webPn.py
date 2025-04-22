from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;from math import nan
from pickle import dump,load
'''
Automatically compress images in current folder and all its subfolders into WebP.
See source code for default parameters. Read cwebp manpage to understand.

Almost in-place conversion. Requires at most 1.5x much space as the biggest image.
If resulting WebP is larger, original picture is kept instead and will not be
converted again on the next run.

Cross-platform support! On android run "pkg install libwebp" in Termux.
Dependencies: cwebp binary on PATH or in current dirrectory
'''
binary='.%scwebp'%sep
if system(binary):
    binary='cwebp'
    if system(binary):
        print('cwebp not found!',file=__import__('sys').stderr);exit();
files={}
formats={'.jpg':'-q 100 -noalpha',
         '.jpeg':'-q 100 -noalpha',
         '.png':'-noalpha -lossless',
         }
try:
    with open('skip.pickle','rb')as f:skip=load(f);print(f'skipping {len(skip)} files')
except:skip=set()
skip2=set()
def gszn(path):
    try:return(s if(s:=getsize(path))>0 else nan)
    except:return nan
def size(n,n2=None):
    if n2:return(size(n)+'->'+size(n2))
    p=0
    while n>1024:n/=1024;p+=1
    return str(round(n,3))+['b','kb','MB','GB','TB'][p]
def globator(dirs,exts):return sum([[i for i in sum([glob('**',root_dir=d,recursive=True)for d in dirs],[])if(gszn(i)!=nan)and i.endswith(x)]for x in exts],[])
fl={i:(i+'.webp')for i in sorted(list(set(globator([getcwd()+sep],['.jpg','.jpeg','.png']))-skip))};n=1;l=len(fl)
for i in fl:
    r=system('%s -quiet %s "%s" -o "%s"'%(binary,formats[i[i.rindex('.'):]],i,fl[i]))
    if r:print(f'{n}/{l} cwebp fail',i)
    else:
        if (b:=gszn(fl[i]))<(a:=gszn(i)):remove(i);print(f'{n}/{l} replace ({size(a,b)}) {fl[i]}')
        else:remove(fl[i]);print(f'{n}/{l} keep {size(a)}',i);skip2.add(i)
    n+=1
skip.update(skip2)
try:
    with open('skip.pickle','wb')as f:dump(skip,f);print('saved skip list')
except:print('fail saving skip list')
input('\nAll done! Press enter to exit.')
exit()


