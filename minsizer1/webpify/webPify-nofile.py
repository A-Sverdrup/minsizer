from glob import glob;from os import getcwd,sep,remove,system;from os.path import getsize;
'''
Automatically compress PNG and JPG files in current folder and its subfolders into WebP.
If resulting WebP is larger than original picture, the original is kept instead.

Dependencies: cwebp binary in current folder
Permissions: write and launch .bat files
'''
def incept(a,b):return sum([sorted(glob(i+b))+incept(sorted(glob(i+'*'+sep)),b)for i in a],[])
fl={i:(i[:-3]+'webp')for i in incept([getcwd()],'*.jpg')}
fl2={i:(i[:-3]+'webp')for i in incept([getcwd()],'*.png')}
for i in fl:system('.%scwebp -q 100 -noalpha "%s" -o "%s"'%(sep,i,fl[i]))
for j in fl2:system('%scwebp -noalpha -lossless "%s" -o "%s"'%(sep,j,fl2[j]))
fl.update(fl2)
for i in fl:
    try:
        if getsize(fl[i])<getsize(i):remove(i);print('replace',fl[i])
        else:remove(fl[i]);print('keep',i)
    except:print('fail',i)
input('\nAll done! Press enter to exit.')
exit()
