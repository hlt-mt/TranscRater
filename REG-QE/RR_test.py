import os
import sys
#import argparse
import numpy as np

from __main__ import *


def main ( testdatadir, modelsdir ):

  if not os.path.exists( testdatadir ):
    print "ERROR!!! test data directory \""+testdatadir+"\" not found"
    return
  if not os.path.exists( modelsdir ):
    print "ERROR!!! model directory \""+modelsdir+"\" not found"
    return
  if not os.path.exists( BASEDIR+"/temp/RR" ):
    os.makedirs( BASEDIR+"/temp/RR" )
  if not os.path.exists( BASEDIR+"/temp/RR/test_label" ):
    os.makedirs( BASEDIR+"/temp/RR/test_label" )
  if not os.path.exists( BASEDIR+"/temp/RR/test_feat" ):
    os.makedirs( BASEDIR+"/temp/RR/test_feat" )
  if not os.path.exists( BASEDIR+"/results" ):
    os.makedirs( BASEDIR+"/results" )
    
  testLabel = BASEDIR+"/temp/RR/test_label/test_label"
  testFeat = BASEDIR+"/temp/RR/test_feat/test_feat"
  resultsdir = BASEDIR+"/results"
  
  label_list = []
  feat_list = []

  for ch in range(CHANNELS):
    if not os.path.exists( testdatadir+"/test_CH_"+str(ch+1)+".wer" ):
      print "Warning!!! WER file "+ testdatadir+"/test_CH_"+str(ch+1)+".wer not found"
      label_list.append( np.zeros([test_size, 1]) )
    else:
      label_list.append( np.nan_to_num(np.genfromtxt( testdatadir+"/test_CH_"+str(ch+1)+".wer",delimiter=' ')) )
    if not os.path.exists( testdatadir+"/test_CH_"+str(ch+1)+"_"+FEAT+".feat" ):
      print "ERROR!!! Feature file "+ testdatadir+"/test_CH_"+str(ch+1)+"_"+FEAT+".feat not found"
      return
    else:
      feat_list.append( np.nan_to_num(np.genfromtxt( testdatadir+"/test_CH_"+str(ch+1)+"_"+FEAT+".feat",delimiter=' ')) )
  

  data_size = label_list[0].shape[0]  
  feat_number = feat_list[0].shape[1]
  
  data_label = np.zeros([CHANNELS*data_size, 1])
  data_feat = np.zeros([CHANNELS*data_size, feat_number])
  for i in range(data_size):
    for ch in range(CHANNELS):
      data_label[i*CHANNELS+ch] = label_list[ch][i] 
      data_feat[i*CHANNELS+ch] = feat_list[ch][i]
      
  np.savetxt( testLabel, data_label , fmt='%.3f') 
  np.savetxt( testFeat, data_feat , fmt='%.4f') 
  
  print "\nTest on Test set: "
  import XRT_REG_test
  XRT_REG_test.main(testFeat, testLabel, modelsdir, resultsdir+"/test.pwer")
  print "Predicted WER are stored in "+ resultsdir+"/test.pwer"
  
if __name__=='__main__':
  sys.exit(main(sys.argv[1]), sys.argv[2])


