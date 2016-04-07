#!/python Convert arrays into untied ranks

import argparse
import math
import numpy as np
from sys import *



infile = argv[1]
channels = int(argv[2])
outfile = argv[3]




if ( infile == "" or channels < 1 or outfile == "" ):
        print "\nERROR!!! Wrong input to \"rank_array.py\"\n"

scores_array = np.nan_to_num(np.genfromtxt(infile,delimiter=' '))

mat = scores_array.reshape(scores_array.shape[0]/channels,channels)

ovlrank = np.argsort(np.mean(mat,axis=0))

mat2 = np.zeros(mat.shape)
for ind in range(mat.shape[1]):
  mat2[:,ind] = mat[:,ovlrank[ind]]

mat3 = mat2.argsort().argsort()

finmat = np.zeros(mat.shape)
for ind in range(mat.shape[1]):
  finmat[:,ovlrank[ind]] = mat3[:,ind]
  
np.savetxt(outfile, finmat+1 , fmt='%d')
  

