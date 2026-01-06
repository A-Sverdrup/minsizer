if __name__!='__main__':raise ImportError("minsizer4 is not a module!")
try:str(exit)
except NameError:from _sitebuiltins import Quitter;exit=Quitter('exit','')
from glob import glob
from os import getcwd,rename,remove,sep
from os.path import exists,getsize,isdir,isfile
from math import nan
from sys import argv,stderr
from time import time,sleep
from pickle import dump,load
__doc__='''\
minsizer4
minsizer4 /?
minsizer4 [-h/--help]
minsizer4 [/MODE <mode>] [/A] [/E] [/Q] [input1] [input2...inputN]
minsizer4 [-m/--mode <mode>] [-a] [-e] [-q] [input1] [input2...inputN]
--------------------------------------------------------------------------------
Automatically compress JPEG/JFIF, PNG, BMP, GIF and TIFF images into WebP or
AVIF using cwebp, gif2webp, avifenc, cavif, tiff2png and bmp2png with the
highest quality possible (lossless or lossy >99%).

Important notices:

PNG:
Unavoidable data loss: APNG is unsupported. APNG animation will be LOST!
Data loss warning:     Alpha-channel is not preserved by default and will be
                       LOST!
Inefficiency:          When preserving alpha-channel, cavif is disabled as it
                       does not support transparency. avifenc is used instead,
                       but it has worse compression ratio.
Compatibility issue:   AVIF files produced by cavif can be incorrectly reported
                       as "corrupted" by Mozilla Firefox and Safari.
BMP:
Data loss warning: If a PNG file with the same name is present in the same
                   folder, it will be LOST. This is an oversight caused by
                   bmp2png and cannot be easily fixed.
GIF:
Compatibility issue: Most software do not support animated WebP.

TIFF:
Data loss warning: Alpha-channel is not preserved by default and will be LOST!
Inefficiency:          When preserving alpha-channel, cavif is disabled as it
                       does not support transparency. avifenc is used instead,
                       but it has worse compression ratio.
Data loss warning: If a PNG file with the same name is present in the same
                   folder, it will be LOST. This is an oversight caused by
                   tiff2png and cannot be easily fixed.

Only the smallest resulting file is kept. If the original (unconverted) file was
kept as smallest, it will not be converted next run (skipped).

Almost in-place conversion. Requires at most 4x as much disk space as the
largest image by file size in the dataset.

Conversion time depends mostly on your hardware and can easily reach multiple
hours and even days when converting large datasets (thousands of pictures).
JPG is faster to convert, PNG is slower and BMP and TIFF are slowest.

Does not accept arguments to pass-through to codecs! Edit source code to see
defaults and tweak codec parameters. See cwebp, gif2webp, avifenc, cavif, 
bmp2png and tiff2png manpages to understand parameters.

Dependencies (cwebp.exe, gif2webp.exe, avifenc.exe, cavif.exe, bmpp2png.exe,
tiff2png.exe) are expected to be found in ./lib subfolder or on PATH

minsizer4: Convert images in current folder and all its subfolders in
           interactive mode
           
minsizer4 [-m/--mode] OR minsizer4 /MODE: Automatic mode: specify filetypes
                                          J/P/B/G/T/*:
                                          J: JPEG/JFIF only
                                          P: PNG only
                                          B: BMP only
                                          G: GIF only
                                          T: TIFF only
                                          *: Everything  except GIF (equivalent
                                          to 'JPBT')
                                          Combinations of above symbols may also
                                          be used, e.g. 'JP' will convert both
                                          JPG and PNG images, 'BPT' will
                                          convert BMP, PNG and TIFF images and
                                          '*G' will convert every supported
                                          image type
                                          
minsizer4 [-a] OR minsizer4 /A: Preserve alpha-channel for PNG and TIFF.

minsizer4 [-e] OR minsizer4 /E: Ignore errors and proceed, do not ask user input
                                to continue.
                                
minsizer4 [-q] OR minsizer4 /Q: Quit after finishing conversion, do not ask user
                                input to exit.

minsizer4 [-h/--help] OR minsizer4 /?: Show this help message and exit.

minsizer4 input1 [input2] ... [inputN]: If input is an image, convert the input
                                        image.
                                        If input is a folder, convert all images
                                        in input folder and all its subfolders. 

minsizer4 dir: Converts all images in <dir> and all its subfolders. 
minsizer4 input: Convert a single image. Sets /MODE to '*' and enables /E
'''
import subprocess
def shell(command):
    startupinfo=subprocess.STARTUPINFO();startupinfo.dwFlags|=subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(command,startupinfo=startupinfo,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL).wait()
if len(argv)==2 and(argv[1]in['/?','-h','--help']):print(__doc__);exit(code=0)
def pause():input('Press Enter to continue (press Ctrl-C to cancel and exit)...')
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:
        print(err%path,file=stderr)
        if not auto:pause()
def test(name,arg,error=None):
    print('Testing for %s...'%name)
    if shell((cwd:=f'.{sep}lib{sep}{name}.exe')+arg):
        if shell(name+arg):
            if error:print(name,'not found!\n',error,file=stderr)
            else:print(name,'not found!',file=stderr);exit(code=1);
        else:print('Using global',name);return name
    else:print('Using local',cwd);return cwd
testPNG=b'\x89PNG\r\n\x1a\nX\rIHDRX\x01X\x01\x08\x02X\x90wS\xdeX\x01sRGBZ\xae\xce\x1c\xe9X\x04gAMAZZ\xb1\x8f\x0b\xfca\x05X\tpHYsZZ\x1d\x87ZZ\x1d\x87\x01\x8f\xe5\xf1eX\x0cIDAT\x18Wc\xf8\xff\xff?Z\x05\xfe\x02\xfe\xa75\x81\x84XZIEND\xaeB`\x82'.replace(b'X',b'ZZZ').replace(b'Z',b'\x00')
testBMP=b'BM:YY\x006Y(Y\x01Y\x01Y\x01\x00\x18Y\x00\x00\x04YYYYYY\x00\xff\xff\xff\x00'.replace(b'Y',b'\x00\x00\x00')
testWEBP=b'RIFF\x1eYYYWEBPVP8L\x11YYY/YYYY\x07\xd0\xff\xfe\xf7\xbf\xff\x81\x88\xe8\x7fYY'.replace(b'Y',b'\x00')
testAVIF=b'X\x1cftypavifYavifmif1miafX\xeametaYX!hdlrYYpictYYYY\x0epitmYZ\x01X"ilocYD@Z\x01Z\x01Y\x01\x0eZ\x01YX\x18X#iinfYZ\x01X\x15infe\x02Y\x01ZZav01YjiprpXKipcoX\x13colrnclxZ\x01Z\rZ\x06\x80X\x0cav1C\x81 \x02Y\x14ispeYX\x01X\x01X\x10pixiY\x03\x08\x08\x08X\x17ipmaYX\x01Z\x01\x04\x01\x82\x03\x04X mdat\x12Z\n\x078Z\x06\x10\x10\xd0i2\x0b\x13@ZZ@Zh\xd2\x14\xc5\x80'.replace(b'X',b'ZZZ').replace(b'Y',b'ZZZZ').replace(b'Z',b'\x00')
testTGA=bytes([0,0,2]+[0]*9+[1,0]*2+[24,32]+[255]*3)
def imgtest(name,arg,content,infile,outfile,error=None):
    with open(infile,'wb')as f:f.write(content)
    binary=test(name,arg,error=error);rmerr(infile,'cannot remove test file!');rmerr(outfile,'cannot remove test file!')
    return binary
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
def getsizenan(path,zero=nan):
    try:return(s if(s:=getsize(path))>0 else zero)
    except:return nan
def endswith(string,end):return string.lower().endswith(tuple(i.lower()for i in end))
def sort(files):return{i:tuple([j for j in files if endswith(j,i)])for i in formats}
def globator(dirs):return[i for i in sum([[d+sep+j for j in glob('**',root_dir=d,recursive=True)]for d in dirs],[])if not(('_files'in i)or('.files'in i)or(getsizenan(i)==nan))]
def size(n,n2=None):
    if n2:return(size(n).rjust(10)+'->'+size(n2).rjust(10))
    p=0
    while n>1024:n/=1024;p+=1
    return str(round(n,3))+' '+['b','kb','MB','GB','TB'][p]
def date(n,n2=None):return('Elapsed:%s ETA:%s'%(date(n),date(n2)))if n2!=None else('%02d:%02d:%02d.%s'%(n//3600,(n//60)%60,n%60,str(n%1)[2:6].ljust(4,'0')))
gbuff=''
tact=0
def pf(*a):global gbuff;print(gbuff+' '.join(a)+' ',end='\r');gbuff+=' '.join(a)+' '
#def tick(*a):global gbuff,tact;print(gbuff+' '+'/|\-'[tact%4]);tact=(tact+1)%4
def pe(*a):global gbuff;print(gbuff+' '.join(a)+' ',end='\n');gbuff=''
def flush():global gbuff;gbuff=''
def fail(path):anomalies.add(path);skip2.add(path);pf('fail(?)','(%s)'%size(getsizenan(path)),path)
def keep(path):skip2.add(path);pf('keep','(%s)'%size(getsizenan(path)),path)
c80=lambda s='':print('\n'+s.center(80,'-'));X=lambda:pf('X');V=lambda:pf('V')
def convert_2_(path,binary,fstring,ext):
    t=-time();pf(binary);I=getsizenan(path)
    if shell(fstring):t+=time();X();keep(path);return t,I,I
    else:
        t+=time();V()
        png=path[:path.rindex('.')]+'.png'
        if(c:=convertPNG(png,nl=None))[3]:
            if getsizenan(png)<I:pf(f'minsized ({size(I,c[2])})',png);rmerr(path);return t+c[0],I,c[2],None,png
            else:keep(path);rmerr(pngpath);return t,I,I,None,path
        else:
            if c[2]<I:
                pf(f'minsized ({size(I,c[2])})')
                try:rename(c[4],(m:=c[4].replace('.png.nl.c.avif',f'.{ext}.avif').replace('.png.nl.avif',f'.{ext}.avif').replace('.png.nl.webp',f'.{ext}.webp')));ny=m
                except:ny=pf(c[4])
                rmerr(path)
                return t+c[0],I,c[2],None,ny
            else:keep(path);rmerr(c[4]);return t,I,I,None,path
def convertPNG(path,nl=True):
    fl={path:getsizenan(path)};t=t0=0;I=getsizenan(path)
    nlc=''if nl else'.nl'
    for b,i,o in [['cavif',f'--lossless -i "{path}" -o "{path}{nlc}.c.avif"',f'{path}{nlc}.c.avif'],
                  ['avifenc',f'-q 100 --qalpha {"100"if alpha else "0"} -d 8 "{path}" -o "{path}{nlc}.avif"',f'{path}{nlc}.avif'],
                  ['cwebp',f'{""if alpha else "-noalpha "}-lossless "{path}" -o "{path}{nlc}.webp"',f'{path}{nlc}.webp']]:#[int(alpha):]:
        if not(B:=binaries[b]):X();continue
        t+=t0;t0=-time();pf(b)
        if shell(B+' '+i):t0+=time();X()
        else:t0+=time();V();fl[o]=getsizenan(o)
    if len(fl)==1:fail(path)
    (M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
    for j in fl:rmerr(j)
    if(m==path)and nl:keep(path)
    elif nl:
        pf(f'minsized ({size(fl[path],M)})')
        if endswith(m,'.c.avif'):
            try:rename(m,(m2:=m.replace('.c.avif','.avif')));m=m2
            except:None
    return t,I,M,m==path,m
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
        if shell(B+' '+i):t0+=time();X()
        else:t0+=time();V();fl[o]=getsizenan(o)
    if len(fl)==1:fail(path)
    (M:=fl.pop(m:=min(fl,key=lambda i:fl[i])))
    for j in fl:rmerr(j)
    if(m==path):keep(path)
    else:pf(f'minsized ({size(fl[path],M)})')
    return t,I,M,m==path,m

############# Codec parameters (See codec manpages to understand) ##############
#
# convert_2_-based: convertTIF and convertBMP
# Parameters must be provided in a specific format:
# 1: path [sic]
# 2: name of binary
# 3: file format extension
#
#
# convert___-based: convertJPG and convertGIF
# Parameters must be provided in a specific format:
# 1: path [sic]
# 2: list of tuples/lists, where each internal tuple/list must contain:
#    - name of codec binary
#    - arguments template: f'<codec arguments> "{path}" -o "{path}.<extension>"'
#    - output filename template: f'{path}.<extension>'
#    e.g. [['somecodecname'.f'{bin} --quiet -quality 100 "{path}" -o "{path}.image"',f'{path}.image']]
#
# convertPNG
# Cannot be configured in a simple way and should not be reconfigured,
# as it is required for convert_2_-based functions to work.
#
def convertTIF(path):
    return convert_2_(path,'tiff2png',f'{binaries["tiff2png"]} "{"."+path[len(getcwd()):]if path.startswith(getcwd())else path}" ','tif')
def convertBMP(path):
    return convert_2_(path,'bmp2png',f'{binaries["bmp2png"]} "{path}" ','bmp')
def convertJPG(path):
    return convert___(path,[['avifenc',f'--qalpha 0 -d 8 "{path}" -o "{path}.avif"',f'{path}.avif'],
                            ['cwebp',f'-q 100 -noalpha "{path}" -o "{path}.webp"',f'{path}.webp']])
def convertGIF(path):
    return convert___(path,[['gif2webp',f'-min_size "{path}" -o "{path}.webp"',f'{path}.webp']])
formats={('.jpg','.jpeg','.jfif'):None,('.png',):None,('.bmp',):None,('.gif',):None,('.tif','.tiff'):None,('.webp',):None,('.avif',):None,}
################################################################################
# Map arguments to formats and formats to conversion function (convert) or None (ignore)
# DO NOT REMOVE convertPNG if you want to convert TIFF and BMP! (it takes 2 steps: tiff -> png -> webp/avif, bmp -> png -> webp/avif)
mappings={'J':('.jpg','.jpeg','.jfif'),
         'P':('.png',),
         'B':('.bmp',),
         'G':('.gif',),
         'T':('.tif','.tiff'),
         'W':('.webp',),
         'A':('.avif',),
         }
converters={('.jpg','.jpeg','.jfif'):convertJPG,
         ('.png',):convertPNG,
         ('.bmp',):convertBMP,
         ('.gif',):convertGIF,
         ('.tif','.tiff'):convertTIF,
         ('.webp',):None,
         ('.avif',):None,
         }
############################### Binaries lookup ################################
# Codec binaries are expected to be in .\lib\ subfolder (local) or
# on PATH (global)
#
# Codec must exit successfully (code=0) to be 'found'.
# Try using help/version argument to test codec.
# If this is impossible or returns wrong exit code, test with imgtest(...)
# instead - a tiny test image will be created, converted and then deleted. 
# You will have to provide your own test file in code though.
binaries={
    'cwebp':test('cwebp',' -version '),
    'avifenc':test('avifenc',' --version '),
    'gif2webp':test('gif2webp',' -version ',error='[.gif] files cannot be converted!'),
    'tiff2png':test('tiff2png','',error='[.tif .tiff] files cannot be converted!'),
    'bmp2png':imgtest('bmp2png',' minsizer-test.bmp',testBMP,'minsizer-test.bmp','minsizer-test.png'),
    'cavif':imgtest('cavif',' -i minsizer-test.png -o minsizer-test.avif ',testPNG,'minsizer-test.png','minsizer-test.avif')
    }
skip2=set();anomalies=set()
def convert(files):
    global formats,auto,mode
    c80()
    try:
        with open('skip.pickle','rb')as f:skip=load(f)
        if skip:print('Skipping files:',*skip,sep='\n')
        else:print('No files to skip.')
    except:skip=set();print('Skip list not found. No files to skip.')
    fl=sort(list(set(files)-skip))
    c80(' Images found: ')
    if mode:
        for i in mode:
            if i in mappings:formats[mappings[i]]=converters[mappings[i]]
            elif i=='*':formats=converters;formats[('.gif',)]=None
        for i in formats:
            if(l:=len(f:=fl[i])):print(f'[{" ".join(i)}]: {l} files ({size(sum(getsizenan(j,0)for j in f))})','to convert'if formats[i]else', nothing to do.')
            else:print('[%s]: No files found'%(' '.join(i)))
        print('Automatic mode: %s Ignore errors: %s Quit after done: %s'%(mode,'NY'[int(auto)],'NY'[int(ex)]))
        for i in range(3):print(f'Starting in {3-i} seconds. If you want to cancel, spam Ctrl-C NOW!',end='\r');sleep(1)
        print('Starting NOW!')
    else:
        buffer={}
        for i in formats:
            if(l:=len(f:=fl[i])):buffer[i]=f'[{" ".join(i)}]: {l} files ({size(sum(getsizenan(j,0)for j in f))})'
            else:buffer[i]='[%s]: No files found'%(' '.join(i))
            print(buffer[i])
        c80()
        if not any(fl.values()):
            print('Nothing to do!')
            if not ex:input('Press enter to exit.')
            exit(code=0)
        for i in(a if(a:=input('Select mode(s) with J/P/B/G/T/* (default=*):'))else'*'):
            if i in mappings:formats[mappings[i]]=converters[mappings[i]]
            elif i=='*':formats=converters;formats[('.gif',)]=None
        c80(' To do: ')
        for i in formats:
            if(l:=len(f:=fl[i])):print(buffer[i],'to convert'if formats[i]else', nothing to do.')
            else:print(buffer[i])
        del buffer
        c80()
        if not auto:pause();auto=(input('Pause on errors (default=Y)? [Y/N]')in['n','N'])
    S=''
    for i in formats:
        try:
            if(l:=len(f:=fl[i]))and formats[i]:
                c80('[%s]: Converting %s files'%(' '.join(i),l));n=1;I=MS=t0=T=0
                for j in f:
                    try:pf(f'{n}/{l} ({size(getsizenan(j))})');t,Is,s,_N,nf=formats[i](j);T+=t;pe(f'{date(t,T*l/n-T)}',nf);I+=Is;MS+=s;n+=1
                    except KeyboardInterrupt:
                        l-=1
                        c80();print('\nInterrupt received - paused');flush()
                        if (choice:=input('Continue (skip file)[1], skip (skip format)[2] or exit[3]? [1/2/3]'))=='1':c80();continue
                        elif choice=='2':c80();break
                        elif choice=='3':raise RuntimeError
                print(m:=f'\n[{" ".join(i)}]: minsized {l} files ({size(I,MS)}), time elapsed: {date(T)}');S+=m
        except RuntimeError:print('Exiting...');c80();break
    c80(' Statistics: ');print(S);c80(' Cleanup: ');
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
    print('\x07\nAll done! ')
    if not ex:input('Press enter to exit.')
    exit(code=0)
def extrargt(name,name2=None):
    if name2:return(extrargt(name)or extrargt(name2))
    elif name in argv:del argv[argv.index(name)];return True
    else:return False
mode=None
for i in ['/MODE','-m','--mode']:
    if i in argv:mode=argv.pop(argv.index(i)+1);del argv[argv.index(i)]
auto=extrargt('/E','-e')
ex=extrargt('/Q','-q')
alpha=extrargt('/A','-a')
if len(argv)==2:
    if isdir(argv[1]):convert(globator([argv[1]]))
    elif isfile(argv[1]):mode='*';auto=True;convert([argv[1]])
    else:print('Unknown error!',file=stderr);exit(code=1)
elif len(argv)>=2:
    muldirs=[];args=[]
    for i in argv:
        if isdir(i):muldirs.append(i)
        elif isfile(i):args.append(i)
    convert(globator(muldirs)+args)
elif len(argv)==1:convert(globator([getcwd()+sep]))
