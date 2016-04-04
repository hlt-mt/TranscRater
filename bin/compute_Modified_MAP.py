#!Python Mean Average Precision for rankings

from __future__ import division

import sys
from sys import exit
import argparse

import numpy as np

if sys.argv[1]:
  true_rank = sys.argv[1]
else:
  print "Error!!! Not defined inputs for MAP ..."
  
if sys.argv[2]:
  pred_rank = sys.argv[2]
else:
  print "Error!!! Not defined inputs for MAP ..."


true_rank_mat = np.nan_to_num(np.genfromtxt(true_rank, delimiter=' '))
pred_rank_mat = np.nan_to_num(np.genfromtxt(pred_rank, delimiter=' '))

if ( true_rank_mat.shape != pred_rank_mat.shape ):
  print "Error!!! Mismatch between True and Predicted ranking files shape"
  exit()

AP_L=[]
for k in range(true_rank_mat.shape[0]):
  trtmp = true_rank_mat[k][true_rank_mat[k].ravel().argsort()]
  prtmp = pred_rank_mat[k][true_rank_mat[k].ravel().argsort()]

  P=[]
  for l in range(true_rank_mat.shape[1]):
    P.append(0)
    for j in range(0,l+1):
      P[l] += (1- (abs(trtmp[j]-prtmp[j]))/true_rank_mat.shape[1]);
    P[l] = P[l]/(l+1)

  AP_L.append(np.sum(P) / true_rank_mat.shape[1])

print np.mean(AP_L)*100



