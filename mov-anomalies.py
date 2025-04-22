from glob import glob;from os import getcwd,sep;from os.path import exists;from sys import argv
'''
Find anomalies - mov files not deleted despite after conversion to mp4
'''
def incepts(a,b):return sorted(sum([sum([glob(i+j)for j in b],[])+incepts(glob(i+'*'+sep),b)for i in a],[]))
print('%s amonalies detected:'%(len(f:=[i for i in incepts([argv[1]+sep],['*.mov'])if any([exists(i[:-4]+j)for j in['.mp4']])])),*f,sep='\n')
input('\nAll done! Press enter to exit.')
exit(code=0)



