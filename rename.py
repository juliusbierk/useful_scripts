import glob
import os
from natsort import natsorted
from collections import Counter

f = glob.glob('*')
c = Counter([x.split('.')[-1] for x in f])
ext = c.most_common(1)[0][0]
f = natsorted(glob.glob('*.'+ext))
i = 0
for fi in f:
	print fi
	os.system('mv %s %06d.%s'%(fi, i, ext))
	i += 1
