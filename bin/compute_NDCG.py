'''
Created on June 9, 2016

@author: jalalvand

compute NDCG at level CHANNELS on the two matrices of rankings.
each of the matrix shows the ranking of each system.
egs:
        s1  s2  s3 ..
  row1   1   3   2   
  row2   3   2   1
  ...
egs:
  compute_NDCG.main( rank_matrix1, rank_matrix2)
'''

from __future__ import division

import sys
import argparse
import math
import numpy as np

  
def main(true_rank_mat, pred_rank_mat):

  if ( true_rank_mat.shape != pred_rank_mat.shape ):
    print "Error!!! Mismatch between True and Predicted ranking files shape"
    exit()

  ndcg=[]

  # for each instance 
  for k in range(true_rank_mat.shape[0]):
    trtmp = true_rank_mat.shape[1] - true_rank_mat[k][true_rank_mat[k].ravel().argsort()] + 1
    prtmp = true_rank_mat.shape[1] - pred_rank_mat[k][true_rank_mat[k].ravel().argsort()] + 1

    # compute ideal dcg
    idcg = 0
    i=1
    for elem in trtmp:
      idcg += (math.pow(2,elem) - 1 ) / math.log(i+1,2)
      i+=1
    
    # compute dcg
    dcg = 0
    i=1
    for elem in prtmp:
      dcg += (math.pow(2,elem) - 1 ) / math.log(i+1,2)
      i+=1
    
    
    ndcg.append( dcg / idcg )
    
  print "NDCG : %.3f" % np.mean(ndcg*100)


if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))


