import os
import glob

format = 'bmp'
in_folder = 'imgs/flag3right'
out_folder = 'imgs/short'
start = 0
stop = 1500


files = glob.glob(in_folder+'/*.'+format)[start:stop]

for f in files:
	print f
	os.system('cp %s %s'%(f,out_folder))