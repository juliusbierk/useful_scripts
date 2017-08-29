import os
import glob

format = 'tif'
in_folder = 'Pos0'
out_folder = 'small'
start = 0
stop = 1500
skip = 2

files = glob.glob(in_folder+'/*.'+format)[start:stop]

for f in files:
	print f
	os.system('cp %s %s'%(f,out_folder))
