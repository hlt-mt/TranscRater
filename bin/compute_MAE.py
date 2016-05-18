#!Python Mean Average Precision for rankings

from __future__ import division

import sys
from sys import exit
import argparse

import numpy as np

if sys.argv[1]:
  test_file = sys.argv[1]
else:
  print "Error!!! Not defined inputs for MAE ..."
  
if sys.argv[2]:
  predWER_file = sys.argv[2]
else:
  print "Error!!! Not defined inputs for MAE ..."


test_file_mat = np.nan_to_num(np.genfromtxt(test_file, delimiter=' '))
pred_wer = np.nan_to_num(np.genfromtxt(predWER_file, delimiter=' '))

if ( test_file_mat.shape[0] != pred_wer.shape[0] ):
  print "Error!!! Mismatch between True and Predicted WER files shape"
  exit()
else:
  print "MAE: %.3f" % np.mean( abs( test_file_mat[:,0] - pred_wer ) )

