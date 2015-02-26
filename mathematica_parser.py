from __future__ import division
import re

s = """
(a^2 eps F \[Pi]^2)/(2 L) + (a^2 A \[Pi]^4)/(2 L^3) - (
 a^4 F \[Pi]^4)/(4 L^3)
"""

expr = s.replace('\n','').replace('[','(').replace(']',') ').replace('\\','')
insert_mult = lambda match: "*".join(match.groups())
expr = re.sub("([0-9])\s*([a-zA-Z])", insert_mult, expr) # '2x' or '2 x'
expr = re.sub("([0-9])\s*([a-zA-Z])", insert_mult, expr) # '2X' or '2 X'
expr = re.sub("([a-zA-Z])\s+([a-zA-Z])", insert_mult, expr) # 'x y', but not 'xy'
expr = re.sub("([a-zA-Z])\s+(\()",    insert_mult, expr) # 'x (', but not 'x('
expr = re.sub("(\))\s*([0-9a-zA-Z])", insert_mult, expr) # ')x', ')2', ') x', etc.
expr = expr.replace(' ','')
expr = expr.replace(')(',')*(')
expr = re.sub("([0-9])(\()", insert_mult, expr) # 2( 
expr = expr.replace('E^','np.exp').replace('Sqrt(','np.sqrt(') \
           .replace('Cos(','np.cos(').replace('Sin(','np.sin(')
expr = expr.replace('^','**')
expr = expr.replace('Pi','np.pi')
expr = expr.replace('(np.pi)','pi')


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

print expr