from glob import glob;from os import getcwd,sep;from os.path import exists;
'''
Find anomalies - faulty webp/avif somehow not removed and still remaining
'''
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
print('%s amonalies detected:'%(len(f:=[i for i in incepts([getcwd()+sep],['*.jpg','*.jpeg','*.png','*.bmp'])if any([exists(i+j)for j in['.avif','.c.avif','.webp']])])),*f,sep='\n')
input('\nAll done! Press enter to exit.')
exit(code=0)



