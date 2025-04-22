if __name__!='__main__':raise ImportError("minsizer3 is not a module!")
from glob import glob
from os import getcwd,rename,remove,sep
from os.path import exists,getsize,isdir
from math import nan
from sys import argv,stderr
from time import time
from pickle import dump,load
__doc__='''\
minsizer3-dryrun
minsizer3-dryrun /?
minsizer3-dryrun [-h/--h/-help/--help]
minsizer3-dryrun input1 [input2] ... [inputN]
minsizer3-dryrun dir
--------------------------------------------------------------------------------
Calculate count and size of JPEG/JFIF, PNG, BMP, GIF and TIFF images that would
be converted by minsizer3 if run with same arguments


minsizer3-dryrun: search for images in current folder and all its subfolders if
                  not provided arguments.
          
minsizer3-dryrun /?:                    Show this help message and exit.
minsizer3-dryrun [-h/--h/-help/--help]: Show this help message and exit.

minsizer3-dryrun input1 [input2] ... [inputN]: Input images.

minsizer3-dryrun dir: Search for images in <dir> and all its subfolders. 

'''
if len(argv)==2 and(argv[1]in['/?','-h','--h','--help','-help']):print(__doc__);exit(code=0)
def rmerr(path,err='Fail removing %s!'):
    try:remove(path)
    except:print(err%path,file=stderr)
def test(name,arg,error=None):
    print('Not testing for %s...'%name)
    return f'.{sep}lib{sep}{name}.exe'
testPNG=b'\x89PNG\r\n\x1a\nX\rIHDRX\x01X\x01\x08\x02X\x90wS\xdeX\x01sRGBZ\xae\xce\x1c\xe9X\x04gAMAZZ\xb1\x8f\x0b\xfca\x05X\tpHYsZZ\x1d\x87ZZ\x1d\x87\x01\x8f\xe5\xf1eX\x0cIDAT\x18Wc\xf8\xff\xff?Z\x05\xfe\x02\xfe\xa75\x81\x84XZIEND\xaeB`\x82'.replace(b'X',b'ZZZ').replace(b'Z',b'\x00')
testBMP=b'BM:YY\x006Y(Y\x01Y\x01Y\x01\x00\x18Y\x00\x00\x04YYYYYY\x00\xff\xff\xff\x00'.replace(b'Y',b'\x00\x00\x00')
testWEBP=b'RIFF\x1eYYYWEBPVP8L\x11YYY/YYYY\x07\xd0\xff\xfe\xf7\xbf\xff\x81\x88\xe8\x7fYY'.replace(b'Y',b'\x00')
testAVIF=b'X\x1cftypavifYavifmif1miafX\xeametaYX!hdlrYYpictYYYY\x0epitmYZ\x01X"ilocYD@Z\x01Z\x01Y\x01\x0eZ\x01YX\x18X#iinfYZ\x01X\x15infe\x02Y\x01ZZav01YjiprpXKipcoX\x13colrnclxZ\x01Z\rZ\x06\x80X\x0cav1C\x81 \x02Y\x14ispeYX\x01X\x01X\x10pixiY\x03\x08\x08\x08X\x17ipmaYX\x01Z\x01\x04\x01\x82\x03\x04X mdat\x12Z\n\x078Z\x06\x10\x10\xd0i2\x0b\x13@ZZ@Zh\xd2\x14\xc5\x80'.replace(b'X',b'ZZZ').replace(b'Y',b'ZZZZ').replace(b'Z',b'\x00')
testTGA=bytes([0,0,2]+[0]*9+[1,0]*2+[24,32]+[255]*3)
def imgtest(name,arg,content,infile,outfile,error=None):
    binary=test(name,arg,error=error)
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
pf=lambda*a:print(*a,end=' ');c80=lambda s:'\n'+s.center(80,'-');X=lambda:print('X',end=' ');V=lambda:print('V',end=' ')
def convertPNG(path,nl=True):pass
def convertTIF(path):pass
def convertBMP(path):pass
def convertJPG(path):pass
def convertGIF(path):pass

################################################################################
# Map formats to conversion function (convert) or None (ignore)
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
# on PATH (global). This version of minsizer3-dryrun does not test for codecs.
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
    print(c80(' Statistics: '));print(S);
    print('This is a dry-run. Nothing was actually converted.\n');
    print(c80(' Cleanup: '));
    input('\nAll done! Press enter to exit.')#Comment to exit automatically (for use in .bat/.sh scripts)
    exit(code=0)
if len(argv)==2:
    if any(endswith(argv[1],i)for i in formats):convert([argv[1]])
    elif sep not in argv[1]:
        if isdir(getcwd()+sep+argv[1]):convert(globator([getcwd()+sep+argv[1]]))
        else:print('Cannot open directory',argv[1],file=stderr);exit(code=1)
    elif sep in argv[1]:
        if isdir(argv[1]):convert(globator([argv[1]]))
        else:print('Cannot open directory',argv[1],file=stderr);exit(code=1)
elif len(argv)>2:convert(argv[1:])
elif len(argv)==1:convert(globator([getcwd()+sep]))
