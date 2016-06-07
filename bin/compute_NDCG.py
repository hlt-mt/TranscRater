#!Python NDCG for rankings

from __future__ import division

import sys
from sys import exit
import argparse
import math
import numpy as np

  
def main(true_rank_mat, pred_rank_mat):

  if ( true_rank_mat.shape != pred_rank_mat.shape ):
    print "Error!!! Mismatch between True and Predicted ranking files shape"
    exit()

  ndcg=[]

  for k in range(true_rank_mat.shape[0]):
    trtmp = true_rank_mat.shape[1] - true_rank_mat[k][true_rank_mat[k].ravel().argsort()] + 1
    prtmp = true_rank_mat.shape[1] - pred_rank_mat[k][true_rank_mat[k].ravel().argsort()] + 1

    idcg = 0
    i=1
    for elem in trtmp:
      idcg += (math.pow(2,elem) - 1 ) / math.log(i+1,2)
      i+=1
      
    dcg = 0
    i=1
    for elem in prtmp:
      dcg += (math.pow(2,elem) - 1 ) / math.log(i+1,2)
      i+=1
    
  #  print  (dcg / idcg)
    ndcg.append( dcg / idcg )
    
  print "NDCG : %.3f" % np.mean(ndcg*100)


if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))


