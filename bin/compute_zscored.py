'''
Created on July 18, 2016

@author: jalalvand

this code computes the zscored feature matrix. 

egs:
  zscored = compute_zscore( input_matrix )
'''
import argparse
import math
import sys
import numpy as np


def main(in_mat):

  out_mat = np.zeros(in_mat.shape)

  means = np.mean (in_mat, axis=0)
  stds  = np.std (in_mat, axis=0)

  for i in range( in_mat.shape[1] ):
    out_mat[:,i] = ( in_mat[:,i] - means[i] ) / stds[i]
  
  return out_mat

if __name__=='__main__':
  sys.exit(sys.argv[1])

