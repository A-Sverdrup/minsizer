from glob import glob;from os import getcwd,sep,startfile,remove;from os.path import getsize;from sys import argv
from pickle import dump,load
'''
Automatically compress PNG and JPG files in current folder and its subfolders into WebP.
If resulting WebP is larger than original picture, the original is kept instead.

Dependencies: cwebp.exe from LibWebP in current folder
Permissions: write and launch .bat files
'''
try:x=argv[1]
except IndexError:x=False
if x:
    try:remove('bat.bat')
    except:None
    with open('fl.pickle','rb')as f:fl=load(f)
    for i in fl:
        if getsize(fl[i])<getsize(i):remove(i);print('replace',fl[i])
        else:remove(fl[i]);print('keep',i)
    try:remove('fl.pickle')
    except:None
    input('\nAll done!')
else:
    def incept(a,b):return sum([sorted(glob(i+b))+incept(sorted(glob(i+'*'+sep)),b)for i in a],[])
    fl={i:(i[:-3]+'webp')for i in incept([getcwd()],'*.jpg')}
    fl2={i:(i[:-3]+'webp')for i in incept([getcwd()],'*.png')}
    bat='\n'.join(['cwebp.exe -q 100 -noalpha "%s" -o "%s"'%(i,fl[i])for i in fl]+['cwebp.exe -noalpha -lossless "%s" -o "%s"'%(j,fl2[j])for j in fl2])+'\nwebPify.py True\npause'
    fl.update(fl2)
    with open('bat.bat','w')as f,open('fl.pickle','wb')as f2:f.write(bat);dump(fl,f2)
    startfile('bat.bat')
    print('Step 1 done!')
