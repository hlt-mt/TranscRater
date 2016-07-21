'''
Created on June 9, 2016

@author: jalalvand

this code converts the WER/scores into rankings. 
The code does not break the rank ties.
For untied ranking use "rank_array.py"

egs:
  ranked_matrix  = rank_array_use_ties( input_matrix )
'''
import argparse
import math
import sys
import numpy as np
from scipy.stats import rankdata


def main(in_mat):

  out_mat = np.zeros(in_mat.shape)
  for i in range(in_mat.shape[0]):
    out_mat[i,:] = rankdata( in_mat[i,:], method='dense' )
    
  return out_mat


if __name__=='__main__':
  sys.exit(sys.argv[1])
      



