from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
from math import nan;from sys import platform,stderr;from time import time
from pickle import dump,load
'''
Automatically compress images in current folder and all its subfolders into WebP or AVIF using cwebp, avifenc and cavif.
Only the smallest file (original/WebP/AVIF/AVIF) is kept. If original file was kept as smallest, it will not be converted next run (skipped).
Almost in-place conversion. Requires at most 3-3.5x as much space as the largest image (by file size, not image dimensions) in the set.

Accepts no arguments. Edit source code to tweak codec parameters.
See cwebp, avifenc and cavif manpages to understand parameters.

Dependencies: cwebp.exe, avifenc.exe and cavif.exe on PATH or in current directory
'''
nil='nul'if platform=='win32'else'/dev/null'
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:print(err%path,file=stderr)
def test(name,arg):
    print('Testing for %s...'%name)
    if system((cwd:='.%s%s'%(sep,name))+arg):
        if system(name+arg):
            print(name,'not found!',file=stderr);exit(code=1);
        else:return name
    else:return cwd
cwebp=test('cwebp',' -version')
avifenc=test('avifenc',' --version')
#gif2webp=test('gif2webp','-version') #Uncomment to enable gif->webp conversion
with open('test.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
cavif=test('cavif',' -i test.png -o test.avif > '+nil);rmerr('test.png','cannot remove test file!');rmerr('test.avif','cannot remove test file!')
params={
      ('*.jpg','*.jpeg','*.jfif'):
          {avifenc:'--qalpha 0 -d 8',
           cwebp:'-q 100 -noalpha'},
      ('*.png',):
          {cavif:'--lossless -i',
           avifenc:'-q 100 --qalpha 0 -d 8',
           cwebp:'-noalpha -lossless'},
      ('*.bmp',):
          {avifenc:'-q 100 --qalpha 0 -d 8',
           cwebp:'-noalpha -lossless'},
#      ('*.gif',):#Uncomment to enable gif->webp conversion
#          {gif2webp:'-min_size'},#Uncomment to enable gif->webp conversion
     }
exts={avifenc:'.avif',cwebp:'.webp',cavif:'.c.avif'}#,gif2webp:'.webp'}
try:
    with open('skip.pickle','rb')as f:skip=load(f)
    if skip:print('Skipping files:',*skip,sep='\n')
    else:print('No files to skip.')
except:skip=set();print('Skip list not found. No files to skip.')
skip2=set();final=''
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
def getsizenan(path):
    try:return(s if(s:=getsize(path))>0 else nan)
    except:return nan
def size(n,n2=None):
    if n2:return'%s -> %s'%(size(n),size(n2))
    p=0
    while n>1024:n/=1024;p+=1
    return '%s %s'%(round(n,3),['b','kb','MB','GB','TB'][p])
def dryrun(ext):
    if(l:=len(f:=list(set(incepts([getcwd()+sep],ext))-skip))):print('%s: %s files (%s) to convert (%s)'%(ext,l,size(sum(getsizenan(i)for i in f)),' '.join(i for i in params[ext])));return True
    else:print('%s: No files found'%(ext,));return False
def cmd(*a):return system('%s %s "%s" -o "%s" > %s 2>&1'%(*a,nil))
def date(n,n2=None):return('Time elapsed:%s ETA:%s'%(date(n),date(n2)))if n2 else('%02d:%02d:%02d.%s'%(n//3600,(n//60)%60,n%60,str(n%1)[2:6]))
def convert(ext):
    print('\n'+('%s: Converting %s files'%(ext,(l:=len(f:=list(set(incepts([getcwd()+sep],ext))-skip))))).center(80,'-'));n=1;I=MS=t0=T=0
    for i in f:
        print('%s/%s'%(n,l),end=' ');fl={i:getsizenan(i)};I+=fl[i];t=0
        for j in params[ext]:
            print(j,end=' ');t0=-time()
            if cmd(j,params[ext][j],i,(w:=i+exts[j])):print('X',end=' ')
            else:fl[w]=getsizenan(w);print('V',end=' ')
            t0+=time();t+=t0
        T+=t;MS+=(M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
        if m==i:skip2.add(i);print('keep %s %s'%(i,date(t,T*l/n-T)))
        else:print('minsized (%s) %s %s'%(size(fl[i],M),m,date(t,T*l/n-T)))
        for j in fl:rmerr(j)
        n+=1
    print(s:='\n%s:minsized %s files (%s), time elapsed: %s'%(ext,l,size(I,MS),date(T)));return s
print('-'*80,*[convert(i)for i in[j for j in params if dryrun(j)]],sep='\n')
if skip2:
    print('Files kept (to skip next run):',*skip2,sep='\n');skip.update(skip2)
    try:
        with open('skip.pickle','wb')as f:dump(skip,f);print('Saved list of files to skip on next run.')
    except:print('Fail saving/updating skip list!')
input('\nAll done! Press enter to exit.')#Comment to exit automatically (for use in .bat/.sh scripts)
exit(code=0)

