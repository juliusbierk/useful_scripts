import glob
import os

f = glob.glob('*.png')
print f

i = 0
for fi in f:
	os.system('mv %s %05d.png'%(fi, i))
	i += 1