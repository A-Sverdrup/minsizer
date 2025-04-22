from glob import glob;from os import getcwd,rename,remove,sep,system;from os.path import exists,getsize;
from math import nan;from sys import argv,platform,stderr;from time import time
from pickle import dump,load
'''
minsizer
minsizer /?
minsizer [-h/--h/-help/--help]
minsizer input1 [input2] ... [inputN]

--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG, BMP and TIFF* images into WebP or AVIF
using cwebp, gif2webp, avifenc, cavif and tiff2png.

Accepts image paths as input arguments. Converts all images in current folder
and all its subfolders if not provided arguments.

*TIFF is only converted to PNG. Run the program again to convert resulting PNG
to WebP/AVIF. TIFF file must be in current directory or its subdirectories,
otherwise tiff2png will fail (tiff2png is badly programmed to only accept
relative paths)

Only the smallest file (original/WebP/AVIF/AVIF) is kept. If the original file
was kept as smallest, it will not be converted next run (skipped).
Almost in-place conversion. Requires at most 3-3.5x as much space as the largest
image (by file size, not image dimensions) in the set.

Does not accept arguments to pass-through to codecs!
Edit source code to tweak codec parameters. See cwebp, gif2webp, avifenc, cavif
and tiff2png manpages to understand parameters.

Dependencies (provided): cwebp.exe, gif2webp.exe, avifenc.exe, cavif.exe,
tiff2png.exe on PATH or in current directory
'''
if len(argv)==2 and argv[1]in['/?','-h','--h','--help','-help']:print(__doc__);exit(code=0)
nil=f'> {"nul"if platform=="win32"else"/dev/null"} 2>&1'
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:print(err%path,file=stderr)
def test(name,arg):
    print('Testing for %s...'%name,end=' ')
    if system((cwd:='.%s%s'%(sep,name))+arg):
        if system(name+arg):
            print(name,'not found!',file=stderr);exit(code=1);
        else:print('global',name);return name
    else:print('local',cwd);return cwd
cwebp=test('cwebp',' -version'+nil)
avifenc=test('avifenc',' --version'+nil)
#gif2webp=test('gif2webp','-version'+nil) #Uncomment to enable gif->webp conversion
tiff2png=test('tiff2png',nil)
with open('test.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
cavif=test('cavif',' -i test.png -o test.avif '+nil);rmerr('test.png','cannot remove test file!');rmerr('test.avif','cannot remove test file!')
stdio='{bin} %s "{input}" -o "{output}"'+nil
class tiffkludge:
    def format(bin,input,output):return f'{bin} {"."+input[len(getcwd()):]if input.startswith(getcwd())else input} '+nil
params={
      ('*.jpg','*.jpeg','*.jfif'):
          {avifenc:stdio%'--qalpha 0 -d 8',
           cwebp:stdio%'-q 100 -noalpha'},
      ('*.png',):
          {cavif:stdio%'--lossless -i',
           avifenc:stdio%'-q 100 --qalpha 0 -d 8',
           cwebp:stdio%'-noalpha -lossless'},
      ('*.bmp',):
          {avifenc:stdio%'-q 100 --qalpha 0 -d 8',
           cwebp:stdio%'-noalpha -lossless'},
      ('*.tif','*.tiff'):
          {tiff2png:tiffkludge},
#      ('*.gif',):#Uncomment to enable gif->webp conversion
#          {gif2webp:stdio%'-min_size'},#Uncomment to enable gif->webp conversion
     }
exts={avifenc:'.avif',cwebp:'.webp',cavif:'.c.avif',tiff2png:'.png'}#,gif2webp:'.webp'}
try:
    with open('skip.pickle','rb')as f:skip=load(f)
    if skip:print('Skipping files:',*skip,sep='\n')
    else:print('No files to skip.')
except:skip=set();print('Skip list not found. No files to skip.')
skip2=set();final=''
#def rext(path,ext,ignore=False):return new if((not exists(new:=(path[:path.rindex('.')]+ext)))or ignore)else(path+ext)
def rext(path,ext,ignore=False):return path[:path.rindex('.')]+ext if path.endswith(('.tif','.tiff'))else(path+ext)
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
def getfl(ext):return([i for i in argv[1:]if any(i.endswith(j[1:])for j in ext)]if len(argv)>1 else list(set(incepts([getcwd()+sep],ext))-skip))
def getsizenan(path):
    try:return(s if(s:=getsize(path))>0 else nan)
    except:return nan
def size(n,n2=None):
    if n2:return'%s -> %s'%(size(n),size(n2))
    p=0
    while n>1024:n/=1024;p+=1
    return '%s %s'%(round(n,3),['b','kb','MB','GB','TB'][p])
def dryrun(ext):
    if(l:=len(f:=getfl(ext))):print('[%s]: %s files (%s) to convert (%s)'%(' '.join(ext),l,size(sum(getsizenan(i)for i in f)),' '.join(i for i in params[ext])));return True
    else:print('[%s]: No files found'%(' '.join(ext)));return False
def date(n,n2=None):return('Time elapsed:%s ETA:%s'%(date(n),date(n2)))if n2 else('%02d:%02d:%02d.%s'%(n//3600,(n//60)%60,n%60,str(n%1)[2:6]))
def c80(s):return '\n'+s.center(80,'-')
def convert(ext):
    print(c80('[%s]: Converting %s files'%(' '.join(ext),(l:=len(f:=getfl(ext))))));n=1;I=MS=t0=T=0
    for i in f:
        print('%s/%s'%(n,l),end=' ');fl={i:getsizenan(i)};I+=fl[i];t=0
        for j in params[ext]:
            print(j,end=' ');t0=-time()
            if system(params[ext][j].format(bin=j,input=i,output=(w:=rext(i,exts[j])))):print('X',end=' ')
            else:fl[w]=getsizenan(w);print('V',end=' ')
            t0+=time();t+=t0
        T+=t;MS+=(M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
        if m==i:skip2.add(i);print(f'keep {i} {date(t,T*l/n-T)}')
        else:print(f'minsized ({size(fl[i],M)}) {m} {date(t,T*l/n-T)}')
        for j in fl:rmerr(j)
        n+=1
    print(s:=f'\n[{" ".join(ext)}]: minsized {l} files ({size(I,MS)}), time elapsed: {date(T)}');return s
print(c80('Images found'))
print(c80('Statistics'),*[convert(i)for i in[j for j in params if dryrun(j)]],sep='\n')
if(l:=len(f:=incepts([getcwd()],['*.c.avif']))):
    print(c80('[*.c.avif]: Renaming %s files to *.avif'%l));n=1
    for i in f:
        print('%s/%s'%(n,l),end=' ')
        try:rename(i,j:=i.replace('.c.avif','.avif'));print('renamed',j)
        except FileExistsError:print('fail',i)
        n+=1
if skip2:
    print(c80('%s files kept (to skip next run):'%len(skip2)),*skip2,sep='\n');skip.update(skip2)
    try:
        with open('skip.pickle','wb')as f:dump(skip,f);print('\nSaved list of files to skip on next run.')
    except:print('\nFail saving/updating skip list!')
if(l:=len(f:=['\n'.join([i]+[i+k for k in['.avif','.c.avif','.webp']if exists(i+k)])for i in incepts([getcwd()+sep],['*.jpg','*.jpeg','*.jfif','*.png','*.bmp','*.gif'])if any([exists(i+j)for j in['.avif','.c.avif','.webp']])])):print(c80('%s amonalies detected:'%len(f)),*f,'Please check these files manually',sep='\n\n')
input('\nAll done! Press enter to exit.')#Comment to exit automatically (for use in .bat/.sh scripts)
exit(code=0)

