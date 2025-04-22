from glob import glob;from os import getcwd,sep,rename
'''
Rename *.c.avif to *.avif
'''
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
l=len(f:=incepts([getcwd()],['*.c.avif']));n=1
for i in f:
    print('%s/%s'%(n,l),end=' ')
    try:rename(i,j:=i.replace('.c.avif','.avif'));print('renamed',j)
    except FileExistsError:print('fail',i)
    n+=1
input('\nAll done! Press enter to exit.')
exit(code=0)

