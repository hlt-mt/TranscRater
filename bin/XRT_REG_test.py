

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

from tempfile import TemporaryFile


if sys.argv[1]:
  test_file = sys.argv[1]
else:
  print "Error!!! No input defined to be Qualified..."
  
if sys.argv[2]:
  qe_models = sys.argv[2]
else:
  print "Error!!! No input defined to be Qualified..."
if sys.argv[3]:
  outfile = sys.argv[3]
else:
  print "Error!!! No output file defined..."
  

X_test = np.nan_to_num(np.genfromtxt(test_file, delimiter=' '))

estimator2 = joblib.load(qe_models+"/XRT.pkl")
scaler = joblib.load(qe_models + "/scaler.pkl")
sel_est = joblib.load(qe_models + "/sel_est.pkl")

X_tests = X_test
X_tests = scaler.transform(X_test)
X_tests = sel_est.transform(X_tests)
y_pred2= np.clip(estimator2.predict(X_tests), 0, 1)

#mae2 = mean_absolute_error(y_test, y_pred2)
#print "Pred2 MAE = %2.8f" % mae2

#print "Predicated WER: ", y_pred2

fout = open(outfile,'w')
for elem in y_pred2:
  fout.write("%.3f\n" % elem)
fout.close()

	
