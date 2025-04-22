if __name__!='__main__':raise ImportError("minsizer3 is not a module!")
from glob import glob
from os import chdir,getcwd,rename,remove,sep,system
from os.path import exists,getsize
from math import nan
from sys import argv,platform,stderr
from time import time
from pickle import dump,load
__doc__='''\
minsizer3
minsizer3 /?
minsizer3 [-h/--h/-help/--help]
minsizer3 input1 [input2] ... [inputN]
minsizer3 dir
--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG*, BMP, GIF** and TIFF* images into WebP or
AVIF using cwebp, gif2webp, avifenc, cavif and tiff2png.

*Caution: APNG and alpha-channel will not be preserved!
**Disabled by default. Edit source code to enable.

Only the smallest resulting file is kept. If the original (unconverted) file was
kept as smallest, it will not be converted next run (skipped).

Almost in-place conversion. Requires at most 4x as much space as the largest
image (by file size, not image dimensions) in the set.


minsizer3: Converts all images in current folder and all its subfolders if not
          provided arguments.
          
minsizer3 /?:                    Show this help messsage and exit.
minsizer3 [-h/--h/-help/--help]: Show this help messsage and exit.

minsizer3 input1 [input2] ... [inputN]: Convert input images.

minsizer3 dir: Converts all images in <dir> and all its subfolders. 

Does not accept arguments to pass-through to codecs! Edit source code to see
defaults and tweak codec parameters. See cwebp, gif2webp, avifenc, cavif and
tiff2png manpages to understand parameters.

Dependencies (provided): cwebp.exe, gif2webp.exe, avifenc.exe, cavif.exe,
tiff2png.exe on PATH or in current directory
'''
if len(argv)==2 and(argv[1]in['/?','-h','--h','--help','-help']):print(__doc__);exit(code=0)
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:print(err%path,file=stderr)
def test(name,arg,error=None):
    print('Testing for %s...'%name)
    if system((cwd:=f'.{sep}lib{sep}{name}')+arg):
        if system(name+arg):
            if error:print(name,'not found!\n',error,file=stderr)
            else:print(name,'not found!',file=stderr);exit(code=1);
        else:print('Using global',name);return name
    else:print('Using local',cwd);return cwd
def imgtest(name,arg,out,error=None):
    with open('test.png','wb')as f:f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x1d\x87\x00\x00\x1d\x87\x01\x8f\xe5\xf1e\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82')
    binary=test(name,arg,error=error);rmerr('test.png','cannot remove test file!');rmerr(out,'cannot remove test file!')
    return binary
def img2test(name,arg,out,error=None):
    with open('test.bmp','wb')as f:f.write(b'BM:YY\x006Y(Y\x01Y\x01Y\x01\x00\x18Y\x00\x00\x04YYYYYY\x00\xff\xff\xff\x00'.replace(b'Y',b'\x00\x00\x00'))
    binary=test(name,arg,error=error);rmerr('test.bmp','cannot remove test file!');rmerr(out,'cannot remove test file!')
    return binary
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
def getsizenan(path,zero=nan):
    try:return(s if(s:=getsize(path))>0 else zero)
    except:return nan
def endswith(string,end):return string.lower().endswith(tuple(i.lower()for i in end))
def sort(files):return{i:tuple([j for j in files if endswith(j,i)])for i in formats}
def globator(dirs):return[i for i in sum([[d+sep+j for j in glob('**',root_dir=d,recursive=True)]for d in dirs],[])if not(('_files'in i)or('.files'in i)or(getsizenan(i)==nan))]
def size(n,n2=None):
    if n2:return(size(n)+'->'+size(n2))
    p=0
    while n>1024:n/=1024;p+=1
    return str(round(n,3))+['b','kb','MB','GB','TB'][p]
def date(n,n2=None):return('Time elapsed:%s ETA:%s'%(date(n),date(n2)))if n2 else('%02d:%02d:%02d.%s'%(n//3600,(n//60)%60,n%60,str(n%1)[2:6]))
def fail(path):anomalies.add(path);skip2.add(path);print('fail(?)','(%s)'%size(getsizenan(path)),path,end=' ')
def keep(path):skip2.add(path);print('keep','(%s)'%size(getsizenan(path)),path,end=' ')
pf=lambda*a:print(*a,end=' ');c80=lambda s:'\n'+s.center(80,'-');X=lambda:print('X',end=' ');V=lambda:print('V',end=' ')
def convertTIF(path):#DO NOT EDIT. NO PARAMETERS TO TWEAK HERE
    t=-time();pf('tiff2png');I=getsizenan(path)
    if system(f'{binaries["tiff2png"]} "{"."+path[len(getcwd()):]if path.startswith(getcwd())else path}" '+nil):t+=time();X();keep(path);return t,I,I
    else:
        t+=time();V()
        if(c:=convertPNG(path[:path.rindex('.')]+'.png',nl=None))[3]:pf(f'minsized ({size(I,c[2])})',path[:path.rindex('.')]+'.png')
        else:
            pf(f'minsized ({size(I,c[2])})')
            try:rename(c[4],(m:=c[4].replace('.png.c.avif','.tif.avif').replace('.png.avif','.tif.avif').replace('.png.webp','.tif.webp')));pf(m)
            except:pf(c[4])
            rmerr(path)
        return t+c[0],I,c[2]
def convertBMP(path):#DO NOT EDIT. NO PARAMETERS TO TWEAK HERE
    t=-time();pf('bmp2png');I=getsizenan(path)
    if system(f'{binaries["bmp2png"]} "{path}" '+nil):t+=time();X();keep(path);return t,I,I
    else:
        t+=time();V()
        if(c:=convertPNG(path[:path.rindex('.')]+'.png',nl=None))[3]:pf(f'minsized ({size(I,c[2])})',path[:path.rindex('.')]+'.png')
        else:
            pf(f'minsized ({size(I,c[2])})')
            try:rename(c[4],(m:=c[4].replace('.png.c.avif','.bmp.avif').replace('.png.avif','.bmp.avif').replace('.png.webp','.bmp.webp')));pf(m)
            except:pf(c[4])
            rmerr(path)
        return t+c[0],I,c[2]
def convertPNG(path,nl=True):
    fl={path:getsizenan(path)};t=t0=0;I=getsizenan(path)
    for b,i,o in [['cavif',f'--lossless -i "{path}" -o "{path}.c.avif"',f'{path}.c.avif'],
                  ['avifenc',f'-q 100 --qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
                  ['cwebp',f'-noalpha -lossless "{path}" -o "{path}.webp"',f'{path}.webp']]:
        if not (B:=binaries[b]):X();continue
        t+=t0;t0=-time();pf(b)
        if system(B+' '+i+nil):t0+=time();X()
        else:t0+=time();V();fl[o]=getsizenan(o)
    if len(fl)==1:fail(path)
    (M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
    for j in fl:rmerr(j)
    if(m==path)and nl:keep(path)
    elif nl:
        pf(f'minsized ({size(fl[path],M)})')
        if endswith(m,'.c.avif'):
            try:rename(m,(m2:=m.replace('.c.avif','.avif')));m=m2;pf(m)
            except:pf(m)
        else:pf(m)
    return((t,I,M)if nl else(t,I,M,m==path,m))
def convert___(path,bio):
    '''bio (binary-input-output) argument must be a list of tuples/lists, where each internal tuple/list must contain:
- name of codec binary
- command prompt template: f'{bin} <codec arguments> "{path}" -o "{path}.<extension>"'
- output filename template: f'{path}.<extension>'
'''
    fl={path:getsizenan(path)};t=t0=0;I=getsizenan(path)
    for b,i,o in bio:
        if not(B:=binaries[b]):continue
        t+=t0;t0=-time();pf(b)
        if system(B+' '+i+nil):t0+=time();X()
        else:t0+=time();V();fl[o]=getsizenan(o)
    if len(fl)==1:fail(path)
    (M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
    for j in fl:rmerr(j)
    if(m==path):keep(path)
    else:pf(f'minsized ({size(fl[path],M)}) {m}')
    return t,I,M
############################### Codec parameters ###############################
# See codec manpages to understand
# See convertTIF and convertPNG above for TIFF and PNG parameters
#
# Parameters must be provided in a sspecific format:
# Must be a list of tuples/lists, where each internal tuple/list must contain:
# - name of codec binary
# - arguments template: f'<codec arguments> "{path}" -o "{path}.<extension>"'
# - output filename template: f'{path}.<extension>'
# e.g. [['somecodecname'.f'{bin} --quiet -quality 100 "{path}" -o "{path}.image"',f'{path}.image']]
#
def convertJPG(path):
    return convert___(path,[['avifenc',f'--qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
                            ['cwebp',f'-q 100 -noalpha "{path}" -o "{path}.webp"',f'{path}.webp']])
#def convertBMP(path):
#    return convert___(path,[['avifenc',f'-q 100 --qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
#                            ['cwebp',f'-noalpha -lossless "{path}" -o "{path}.webp"',f'{path}.webp']])
def convertGIF(path):
    return convert___(path,[['gif2webp',f'-min_size "{path}" -o "{path}.webp"',f'{path}.webp']])

################################################################################
# Map formats to conversion function (convert) or None (ignore)
# DO NOT REMOVE convertPNG if you want to convert TIFF!
# (it is a 2-step process: tiff -> png -> webp/avif)
formats={('.jpg','.jpeg','.jfif'):convertJPG,
         ('.png',):convertPNG,
         ('.bmp',):convertBMP,
         ('.gif',):None,
#         ('.gif',):convertGIF, #Uncomment to enable gif->webp
         ('.tif','.tiff'):convertTIF,
         ('.webp',):None,
         ('.avif',):None,
         }
############################### Binaries lookup ################################
# Codec binaries are expected to be in .\lib\ subfolder (local) or
# on PATH (global)
#
# Codec must exit successfully (code=0) to be 'found'.
# Use help/version argument to test this if possible.
# If impossible or help/version returns wrong exit code, imgtest instead
# (a tiny png file will be created, converted and then deleted)

nil=f'> {"nul"if platform=="win32"else"/dev/null"} 2>&1' # Null device lookup 
#nil='>>log.log 2>>error.log' #Uncomment to enable logging (not recommended)
#nil='' #Uncomment to enable verbose output (very not recommended)
binaries={
    'cwebp':test('cwebp',' -version '+nil),
    'avifenc':test('avifenc',' --version '+nil),
    'gif2webp':test('gif2webp',' -version '+nil,error='[.gif] files cannot be converted!'),
    'tiff2png':test('tiff2png',nil,error='[.tif .tiff] files cannot be converted!'),
    'bmp2png':img2test('bmp2png',' test.bmp'+nil,'test.png'),
    'cavif':imgtest('cavif',' -i test.png -o test.avif '+nil,'test.avif')
    }
skip2=set();anomalies=set()
def convert(files):
    print('-'*80)
    try:
        with open('skip.pickle','rb')as f:skip=load(f)
        if skip:print('Skipping files:',*skip,sep='\n')
        else:print('No files to skip.')
    except:skip=set();print('Skip list not found. No files to skip.')
    fl=sort(files);print(c80(' Images found: '))
    for i in formats:
        if(l:=len(f:=fl[i])):print(f'[{" ".join(i)}]: {l} files ({size(sum(getsizenan(j,0)for j in f))})','to convert'if formats[i]else', nothing to do.')
        else:print('[%s]: No files found'%(' '.join(i)))
    S=''
    if not any(fl.values()):
        input('Nothing to do! Press enter to exit.')#Comment to exit automatically (for use in .bat/.sh scripts)
        exit(code=0)
    for i in formats:
        if(l:=len(f:=fl[i]))and formats[i]:
            print(c80('[%s]: Converting %s files'%(' '.join(i),l)));n=1;I=MS=t0=T=0
            for j in f:pf(f'{n}/{l}');t,Is,s=formats[i](j);T+=t;print(f'{date(t,T*l/n-T)}');I+=Is;MS+=s;n+=1
            print(m:=f'\n[{" ".join(i)}]: minsized {l} files ({size(I,MS)}), time elapsed: {date(T)}');S+=m
    print(c80(' Statistics: '));print(S);print(c80(' Cleanup: '));
    if skip2:
        print('Files kept (to skip next run):',*skip2,sep='\n');skip.update(skip2)
        try:
            with open('skip.pickle','wb')as f:dump(skip,f);print('Saved list of files to skip on next run.')
        except:print('Fail saving/updating skip list!')
    else:print('No files to skip on next run')
    if anomalies:print('%s files failed to convert:'%len(anomalies),*anomalies,'\nThese files may be corrupted.\nPlease check them manually',sep='\n')
    else:print('No failures detected')
    if(l:=len(f:=['\n'.join([i]+[i+k for k in['.avif','.c.avif','.webp']if exists(i+k)])for i in incepts([getcwd()+sep],['*.jpg','*.jpeg','*.jfif','*.png','*.bmp','*.gif'])if any([exists(i+j)for j in['.avif','.c.avif','.webp']])])):print('%s amonalies detected:'%len(f),*f,'Please check these files manually',sep='\n\n')
    else:print('No anomalies detected')
    input('\nAll done! Press enter to exit.')#Comment to exit automatically (for use in .bat/.sh scripts)
    exit(code=0)
if len(argv)==2:
    if any(endswith(argv[1],i)for i in formats):convert([argv[1]])
    elif sep not in argv[1]:
        if exists(getcwd()+sep+argv[1]):convert(globator([getcwd()+sep+argv[1]]))
        else:print('Cannot open directory',argv[1],file=stderr);exit(code=1)
    elif sep in argv[1]:
        if exists(argv[1]):convert(globator([argv[1]]))
        else:print('Cannot open directory',argv[1],file=stderr);exit(code=1)
elif len(argv)>2:convert(argv[1:])
elif len(argv)==1:convert(globator([getcwd()+sep]))
