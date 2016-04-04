

import sys

import argparse
import os
import codecs
import glob
import math

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics.metrics import mean_absolute_error, mean_squared_error
from sklearn.externals import joblib

import numpy as np

from tempfile import TemporaryFile


if sys.argv[1]:
  test_file = sys.argv[1]
else:
  print "Error!!! No input defined to be Qualified..."
  
if sys.argv[2]:
  qe_models = sys.argv[2]
else:
  print "Error!!! No input defined to be Qualified..."

#if sys.argv[3]:
#  outputfile = sys.argv[3]
#else:
#  print "Error!!! No output file defined..."
  

X_test = np.nan_to_num(np.genfromtxt(test_file, delimiter=' '))
#y_test = np.clip(np.genfromtxt('data/REG/testLabel/Tst-Real-New-jan25_1.ctm.wer'), 0, 1)

estimator2 = joblib.load(qe_models+"/XRT.pkl")
scaler = joblib.load(qe_models + "/scaler.pkl")
sel_est = joblib.load(qe_models + "/sel_est.pkl")

X_tests = X_test
X_tests = scaler.transform(X_test)
#print "Scaler \n", X_tests
X_tests = sel_est.transform(X_tests)
#print "Sel_est \n", X_tests
y_pred2= np.clip(estimator2.predict(X_tests), 0, 1)

#mae2 = mean_absolute_error(y_test, y_pred2)
#print "Pred2 MAE = %2.8f" % mae2

#print "Predicated WER: ", y_pred2


for elem in y_pred2:
  print  elem

#np.savetxt("results/REG/Tst-Real-New-jan25_1.predWER", y_pred2, fmt="%.3f")
	
