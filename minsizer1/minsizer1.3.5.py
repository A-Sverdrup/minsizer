from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
from math import nan;from sys import platform,stderr
from pickle import dump,load
'''
Automatically compress images in current folder and all its subfolders into WebP or AVIF using cwebp, avifenc and cavif.
Only the smallest file (original/WebP/AVIF/AVIF) is kept. If original file was kept as smallest, it will not be converted next run (skipped).
Almost in-place conversion. Requires at most 3-3.5x as much space as the largest image (by file size, not image dimensions) in the set.

Accepts no arguments. Edit source code to tweak codec parameters.
See source code for default parameters. See cwebp, avifenc and cavif manpages to understand parameters

Dependencies: cwebp.exe, avifenc.exe and cavif.exe on PATH or in current directory
'''
nil='nul'if platform=='win32'else'/dev/null'
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:print(err%path,file=stderr)
def test(name,arg):
    if system((cwd:='.%s%s'%(sep,name))+arg):
        if system(name+arg):
            print(name,'not found!',file=stderr);exit(code=1);
        else:return name
    else:return cwd
def testavif(name,i=''):
    with open('test.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
    res=test(name,i+' test.png -o test.avif > '+nil)
    rmerr('test.png','cannot remove test file!');rmerr('test.avif','cannot remove test file!')
    return res
cwebp=test('cwebp',' > '+nil)
cavif=testavif('cavif',i=' -i')
avifenc=testavif('avifenc')
formats={
      ('*.jpg','*.jpeg'):
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
    with open('skip.pickle','rb')as f:skip=load(f);print('Skipping files:',*skip,sep='\n')
except:skip=set();print('No files to skip.')
skip2=set()
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
def cmd(*a):return system('%s %s "%s" -o "%s" > %s 2>&1'%(*a,nil))
def getsizenan(path):
    try:return getsize(path)
    except:return nan
def convert(ext):
    l=len(f:=list(set(incepts([getcwd()+sep],ext))-skip));n=1
    for i in f:
        fl={i:getsizenan(i)}
        for j in formats[ext]:
            print(j,end=' ')
            if cmd(j,formats[ext][j],i,(w:=i+exts[j])):None
            else:fl[w]=getsizenan(w)
        M=fl.pop(m:=min(fl,key=lambda i:fl[i]))
        if m==i:skip2.add(i);print('\n%s/%s keep'%(n,l),i)
        else:print('\n%s/%s minsized (%s->%s)'%(n,l,fl[i],M),m)
        for j in fl:rmerr(j)
        n+=1
for i in formats:convert(i)
if skip2:
    skip.update(skip2)
    try:
        with open('skip.pickle','wb')as f:dump(skip,f);print('Saved list of files to skip on next run.')
    except:print('Fail saving/updating skip list!')
input('\nAll done! Press enter to exit.')
exit(code=0)

