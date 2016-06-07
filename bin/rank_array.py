#!/python Convert arrays into untied ranks

import argparse
import math
import sys
import numpy as np

from __main__ import *

def main(in_mat):

  ovlrank = np.argsort(np.mean(in_mat,axis=0))

  mat2 = np.zeros(in_mat.shape)
  for ind in range(in_mat.shape[1]):
    mat2[:,ind] = in_mat[:,ovlrank[ind]]

  mat3 = mat2.argsort().argsort()

  out_mat = np.zeros(in_mat.shape)
  for ind in range(in_mat.shape[1]):
    out_mat[:,ovlrank[ind]] = mat3[:,ind]
    
  return out_mat+1


if __name__=='__main__':
  sys.exit(sys.argv[1])
      



