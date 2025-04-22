from glob import glob
from os import getcwd,sep,remove
from os.path import exists,getsize;from sys import argv
__doc__='''\
cmp-rm [-dir DIR] SOURCE RESULT [+] [-minsize]

Recursively search for files with extensions SOURCE and RESULT.
If RESULT is larger than SOURCE, prompt to remove RESULT.

-dir: specify work directory (current directory if unspecified)
SOURCE: original file format
RESULT: resulting file format
+: compare filename.SOURCE.RESULT instead of filename.RESULT to filename.SOURCE
-minsize: Also remove SOURCE if SOURCE is larger then RESULT
'''
plus=minsize=False
if'-dir'in argv:dir=argv.pop(argv.index('-dir')+1);argv.remove('-dir')
else:dir=getcwd()
if'+'in argv:plus=True;argv.remove('+')
if'-minsize'in argv:minsize=True;argv.remove('-minsize')
argv=[(i.replace('*.','')if i.startswith(('*.','.'))else i)for i in argv[1:]]
if(not argv)or(len(argv)!=2):print(__doc__);exit(code=0)
l=[]
def getsizenan(path):
    try:return(s if(s:=getsize(path))>0 else nan)
    except:return nan
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
for i in incepts([dir+sep],['*.'+argv[0]]):
    if exists(j:=((i+argv[1])if plus else(i[:i.rindex('.')+1]+argv[1]))):
        if getsizenan(j)>getsizenan(i):l.append(j);print(j,'is larger than source!')
        elif minsize and(getsizenan(i)>getsizenan(j)):l.append(i);print(i,'is larger than result!')
if l and input('delete?')=='delete':
    for i in l:
        try:remove(i);print('removed',i)
        except:print('Fail removing %s!'%i,file=stderr)
exit(code=0)



