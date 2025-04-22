if __name__!='__main__':raise ImportError("minsizer2 is not a module!")
try:str(exit)
except NameError:from _sitebuiltins import Quitter;exit=Quitter('exit','')
from glob import glob;from os import getcwd,rename,remove,sep,system;from os.path import exists,getsize;
from math import nan;from sys import argv,platform,stderr;from time import time
from pickle import dump,load
'''
minsizer2
minsizer2 /?
minsizer2 [-h/--h/-help/--help]
minsizer2 input1 [input2] ... [inputN]
--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG*, BMP and TIFF** images into WebP or AVIF
using cwebp, gif2webp, avifenc, cavif and tiff2png.
Accepts image paths as input arguments. Converts all images in current folder
and all its subfolders if not provided arguments.
*  Caution: APNG and alpha-channel will not be preserved!
** TIFF must be in current working directory or its subdirectories, otherwise
tiff2png will fail (tiff2png is badly programmed to only accept relative paths).
If providing TIFF as argument, make sure to cd there first.
Only the smallest resulting file is kept. If the original unconverted file was
kept as smallest, it will not be converted next run (skipped).
Almost in-place conversion. Requires at most 4x as much space as the largest
image (by file size, not image dimensions) in the set.
Does not accept arguments to pass-through to codecs!
Edit source code to see defaults and tweak codec parameters. See cwebp,
gif2webp, avifenc, cavif and tiff2png manpages to understand parameters.
Dependencies (provided): cwebp.exe, gif2webp.exe, avifenc.exe, cavif.exe,
tiff2png.exe on PATH or in current directory
'''
if len(argv)==2 and argv[1]in['/?','-h','--h','--help','-help']:print(__doc__);exit(code=0)
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:print(err%path,file=stderr)
def test(name,arg):
    print('Testing for %s...'%name)
    if system((cwd:=f'.{sep}lib{sep}{name}')+arg):
        if system(name+arg):
            print(name,'not found!',file=stderr);exit(code=1);
        else:print('Using global',name);return name
    else:print('Using local',cwd);return cwd
nil=f'> {"nul"if platform=="win32"else"/dev/null"} 2>&1' # Testing for null device 
#nil='>>log.log 2>>error.log'
cwebp=test('cwebp',' -version '+nil)# Testing for binaries on pwd or PATH
avifenc=test('avifenc',' --version '+nil)
gif2webp=test('gif2webp',' -version '+nil)
tiff2png=test('tiff2png',nil)
with open('test.png','wb')as f:f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82")
cavif=test('cavif',' -i test.png -o test.avif '+nil);rmerr('test.png','cannot remove test file!');rmerr('test.avif','cannot remove test file!')
print('-'*80)
def rext(path,ext,ignore=False):return new if((not exists(new:=(path[:path.rindex('.')]+ext)))or ignore)else(path+ext)
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
def getfl(ext):return([i for i in argv[1:]if any(i.endswith(j[1:])for j in ext)]if len(argv)>1 else list(set(incepts([getcwd()+sep],ext))-skip))
def getsizenan(path):
    try:return(s if(s:=getsize(path))>0 else nan)
    except:return nan
def size(n,n2=None):
    if n2:return(size(n)+'->'+size(n2))
    p=0
    while n>1024:n/=1024;p+=1
    return str(round(n,3))+['b','kb','MB','GB','TB'][p]
def date(n,n2=None):return('Time elapsed:%s ETA:%s'%(date(n),date(n2)))if n2 else('%02d:%02d:%02d.%s'%(n//3600,(n//60)%60,n%60,str(n%1)[2:6]))
def keep(path):skip2.add(path);print('keep',size(getsizenan(path)),path,end=' ')
pf=lambda*a:print(*a,end=' ');c80=lambda s:'\n'+s.center(80,'-');X=lambda:print('X',end=' ');V=lambda:print('V',end=' ')
def convertTIF(path):
    t=-time();pf('tiff2png');I=getsizenan(path)
    if system(f'{tiff2png} "{"."+path[len(getcwd()):]if path.startswith(getcwd())else path}" '+nil):t+=time();X();keep(i);return n+1,t,I
    else:
        t+=time();V()
        if(c:=convertPNG(path[:path.rindex('.')]+'.png',nl=None))[3]:pf(f'minsized ({size(I,c[2])})',path[:path.rindex('.')]+'.png')
        else:
            pf(f'minsized ({size(I,c[2])})')
            try:rename(c[4],(m:=c[4].replace('.png.c.avif','.tif.avif').replace('.png.avif','.tif.avif').replace('.png.webp','.tif.webp')));pf(m)
            except:pf(c[4])
            rmerr(path)
        return t+c[0],I,c[2]
def convertPNG(path,nl=True):
    fl={path:getsizenan(path)};t=t0=0;I=getsizenan(path)
    for b,i,o in [['cavif',f'{cavif} --lossless -i "{path}" -o "{path}.c.avif"',f'{path}.c.avif'],
                  ['avifenc',f'{avifenc} -q 100 --qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
                  ['cwebp',f'{cwebp} -noalpha -lossless "{path}" -o "{path}.webp"',f'{path}.webp']]:
        t+=t0;t0=-time();pf(b)
        if system(i+nil):t0+=time();X()
        else:t0+=time();V();fl[o]=getsizenan(o)
    (M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
    for j in fl:rmerr(j)
    if(m==path)and nl:keep(i)
    elif nl:
        pf(f'minsized ({size(fl[path],M)})')
        if m.endswith('.c.avif'):
            try:rename(m,(m2:=m.replace('.c.avif','.avif')));m=m2;pf(m)
            except:pf(m)
    return((t,I,M)if nl else(t,I,M,m==path,m))
def convert___(path,bio):
    fl={path:getsizenan(path)};t=t0=0;
    for b,i,o in bio:
        t+=t0;t0=-time();pf(b)
        if system(i+nil):t0+=time();X()
        else:t0+=time();V();fl[o]=getsizenan(o)
    (M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
    if(m==path)and nl:keep(path)
    else:pf(f'minsized ({size(fl[path],M)}) {m}')
    for j in fl:rmerr(j)
    return t,fl[path],M
def convertJPG(path):
    return convert___(path,[['avifenc',f'{avifenc} --qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
                            ['cwebp',f'{cwebp} -q 100 -noalpha "{path}" -o "{path}.webp"',f'{path}.webp']])
def convertBMP(path):
    return convert___(path,[['avifenc',f'{avifenc} -q 100 --qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
                            ['cwebp',f'{cwebp} -noalpha -lossless "{path}" -o "{path}.webp"',f'{path}.webp']])
def convertGIF(path):
    t=-time();pf('gif2webp');I=getsizenan(path)
    if system(f'{gif2webp} "{path}" -o "{path}.webp"'+nil):t+=time();X();keep(i);return t,I,I
    else:
        t+=time();V()
        if(s2:=getsizenan(f'{path}.webp'))<I:pf(f'minsized ({size(I,s2)}) {path}.webp');rmerr(path);return t,I,s2
        else:keep(i);rmerr(f'{path}.webp');return t,I,I
formats={'jpg':('*.jpg','*.jpeg','*.jfif'),'png':('*.png',),'bmp':('*.bmp',),'gif':('*.gif',),'tif':('*.tif','*.tiff'),'webp':('*.webp',),'avif':('*.avif',)}
methods={'jpg':convertJPG,'png':convertPNG,'bmp':convertBMP,'tif':convertTIF,
         'gif':None,'webp':None,'avif':None}
def convert():
    S=''
    for i in formats:
        if(l:=len(f:=getfl(formats[i])))and methods[i]:
            print(c80('[%s]: Converting %s files'%(' '.join(formats[i]),l)));n=1;I=MS=t0=T=0
            for j in f:pf(f'{n}/{l}');t,Is,s=methods[i](j);T+=t;print(f'{date(t,T*l/n-T)}');I+=Is;MS+=s;n+=1
            print(m:=f'\n[{" ".join(formats[i])}]: minsized {l} files ({size(I,MS)}), time elapsed: {date(T)}');S+=m
        else:print(c80('[%s]: Nothing to do'%' '.join(formats[i])))
    print(c80(' Statistics: '));print(S)
def dryrun():
    print(c80(' Images found: '))
    for i in formats:
        if(l:=len(f:=getfl(formats[i]))):print(f'[{" ".join(formats[i])}]: {l} files ({size(sum(getsizenan(i)for i in f))})','to convert'if methods[i]else', nothing to do.')
        else:print('[%s]: No files found'%(' '.join(formats[i])))
try:#Skip list
    with open('skip.pickle','rb')as f:skip=load(f)
    if skip:print('Skipping files:',*skip,sep='\n')
    else:print('No files to skip.')
except:skip=set();print('Skip list not found. No files to skip.')
skip2=set();dryrun();convert()
if skip2:
    print('Files kept (to skip next run):',*skip2,sep='\n');skip.update(skip2)
    try:
        with open('skip.pickle','wb')as f:dump(skip,f);print('Saved list of files to skip on next run.')
    except:print('Fail saving/updating skip list!')
if(l:=len(f:=['\n'.join([i]+[i+k for k in['.avif','.c.avif','.webp']if exists(i+k)])for i in incepts([getcwd()+sep],['*.jpg','*.jpeg','*.jfif','*.png','*.bmp','*.gif'])if any([exists(i+j)for j in['.avif','.c.avif','.webp']])])):print('%s amonalies detected:'%len(f),*f,'Please check these files manually',sep='\n\n')
input('\nAll done! Press enter to exit.')#Comment to exit automatically (for use in .bat/.sh scripts)
exit(code=0)
