
import sys

import argparse
import os
import codecs
import glob
import math

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.externals import joblib

import numpy as np

from __main__ import *


def main (test_feat, test_label, qe_models, outfile):

  print "Test on %s ..." % test_feat
  
  X_feat = np.nan_to_num(np.genfromtxt(test_feat, delimiter=' '))
  X_label = np.nan_to_num(np.genfromtxt(test_label, delimiter=' '))
  
  estimator2 = joblib.load(qe_models+"/XRT.pkl")
  scaler = joblib.load(qe_models + "/scaler.pkl")
  sel_est = joblib.load(qe_models + "/sel_est.pkl")

  X_tests = X_feat
  X_tests = scaler.transform(X_feat)
  X_tests = sel_est.transform(X_tests)
  y_pred = estimator2.predict(X_tests)

  
  print "MAE : %.3f" % mean_absolute_error(X_label, y_pred)
  np.savetxt( outfile, y_pred , fmt='%.3f') 
  
  if CHANNELS > 1:
    import rank_array
    true_rank_mat =      rank_array.main( X_label.reshape([X_label.shape[0]/CHANNELS, CHANNELS]) ) 
    pred_rank_mat = rank_array.main( y_pred.reshape([y_pred.shape[0]/CHANNELS, CHANNELS]) )
    import compute_NDCG
    compute_NDCG.main(true_rank_mat, pred_rank_mat)
  
  
if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2],sys.argv[3]))
  
  	
