from __future__ import division
import re

s = """
((dt kb + xib) (dt F20 + db2p xib) + 
 cb dt (dt (F10 + F20) + (db1p + db2p) xib))/((dt kb + xib) (2 cb dt +
    dt kb + xib))
"""

expr = s.replace('\n','').replace('[','(').replace(']',') ').replace('\\','')
insert_mult = lambda match: "*".join(match.groups())
expr = re.sub("([0-9])\s*([a-zA-Z])", insert_mult, expr) # '2x' or '2 x'
expr = re.sub("([0-9])\s*([a-zA-Z])", insert_mult, expr) # '2X' or '2 X'
expr = re.sub("([a-zA-Z])\s+([a-zA-Z])", insert_mult, expr) # 'x y', but not 'xy'
expr = re.sub("([a-zA-Z])\s+(\()",    insert_mult, expr) # 'x (', but not 'x('
expr = re.sub("(\))\s*([0-9a-zA-Z])", insert_mult, expr) # ')x', ')2', ') x', etc.
expr = re.sub("([a-zA-Z])\s+([a-zA-Z])", insert_mult, expr) # 'x y', but not 'xy'
expr = expr.replace(' ','')
expr = expr.replace(')(',')*(')
expr = re.sub("([0-9])(\()", insert_mult, expr) # 2( 
expr = expr.replace('E^','np.exp').replace('Sqrt(','np.sqrt(') \
           .replace('Cos(','np.cos(').replace('Sin(','np.sin(')
expr = expr.replace('Pi','np.pi')
expr = expr.replace('{','[')
expr = expr.replace('}',']')
expr = expr.replace('Abs','np.abs')
expr = expr.replace('Cot','cot')
expr = expr.replace('Csc','csc')
expr = expr.replace('Sec','sec')
expr = expr.replace('BesselI','iv')
expr = expr.replace('Erfc','erfc')
expr = expr.replace('Erf','erf')
expr = expr.replace('(Sqrt)*(','np.sqrt(')

def cot(x):
  return 1./np.tan(x)
def sec(x):
  return 1./np.cos(x)
def csc(x):
  return 1./np.sin(x)

### divide over lines:
count = 0
last_i = -1
indeces = []
for i, s in enumerate(expr):
  count +=1
  if count > 80 and last_i > 0:
    count = 0
    indeces.append(last_i)
    last_i = -1
  if s in ['+','-','*','/']:
    last_i = i
expr = "".join([(s+' \\\n' if i in indeces else s) for i,s in enumerate(expr)])
expr = expr.replace('^','**')

print expr
