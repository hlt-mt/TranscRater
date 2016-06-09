'''
Created on June 9, 2016

@author: jalalvand

this code converts the WER/scores into rankings. 
The code breaks the rank ties by computing the 
average of the scores for each component.

egs:
  rank_array( input_matrix )
'''
import argparse
import math
import sys
import numpy as np

from __main__ import *

def main(in_mat):

  # compute the overal rank of each system (column) on whole rows
  ovlrank = np.argsort(np.mean(in_mat,axis=0))

  # swap the columns based on the overal ranks
  mat2 = np.zeros(in_mat.shape)
  for ind in range(in_mat.shape[1]):
    mat2[:,ind] = in_mat[:,ovlrank[ind]]

  # compute the untied ranks
  mat3 = mat2.argsort().argsort()

  # swap the columns to the original positions
  out_mat = np.zeros(in_mat.shape)
  for ind in range(in_mat.shape[1]):
    out_mat[:,ovlrank[ind]] = mat3[:,ind]
    
  return out_mat+1


if __name__=='__main__':
  sys.exit(sys.argv[1])
      



