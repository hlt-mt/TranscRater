

import sys
from sys import exit
from scipy import stats
import argparse
import math
import numpy as np



def loadsvmlight(f):

  label=[] 
  qid=[]
  data=[]
    
  infile = open(f,'r')
  for elem in infile:
    el = elem.split()
    label.append(el[0])
    qid.append(el[1])
    tmp=[]
    for e in el[2:]:
      tmp.append(float(e.split(':')[1]))
    if not np.array(data).size:
      data = np.array(tmp)
    else:
      data = np.vstack([data, np.array(tmp)])

  infile.close()    
  data = stats.zscore(data, ddof=1)
  data[np.isnan(data)] = 0
  
  return label, qid, data


inname = sys.argv[1]
outname = sys.argv[2]

a, b, c = loadsvmlight(inname)

c = stats.zscore(c, ddof=1)

c[np.isnan(c)] = 0

outfile = open(outname,'w')
for i in range(len(a)):
  outfile.write('%s ' % a[i])
  outfile.write('%s ' % b[i])
  for j in range(c.shape[1]):
    outfile.write("%d:%f " % (j+1 , c[i,j]) )
  outfile.write('\n')

outfile.close() 


