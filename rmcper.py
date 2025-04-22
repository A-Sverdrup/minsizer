from glob import glob;from os import sep,remove;from os.path import getsize,exists;
from sys import argv,stderr;from argparse import ArgumentParser
'''
Compare and remove original JPG/PNG/BMP images converted to AVIF/WEBP on other disk.
Other disk MUST have same folder structure!
'''
arg=ArgumentParser(description='',epilog='')
arg.add_argument('input',metavar='INPUT',help='Input disk letter')
arg.add_argument('output',metavar='OUTPUT',help='Output disk letter')
arg.add_argument('-dir',dest='dir',default='',metavar='SUBDIR',help='Subdirectory (disk root if unspecified)',required=False)
args=arg.parse_args()
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
f=[args.output[0]+i[1:].replace('.c.avif','').replace('.avif','').replace('.webp','')for i in incepts(['%s:%s%s'%(args.input[0],sep,args.dir)],['*.avif','*.webp'])]
l=len(f);n=1
for i in f:
    print('%s/%s'%(n,l),end=' ')
    if exists(i):
        try:remove(i),print('del',i)
        except:print('fail',i)
    else:print('not found',i)
    n+=1
input('\nAll done! Press enter to exit.')
exit(code=0)

