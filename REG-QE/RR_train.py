#!/usr/bin/env python Prepare the words for LM feature extraction

import os
import sys
import argparse
import numpy as np

from __main__ import *


def main ( traindatadir, modelsdir ):
  
  if not os.path.exists( traindatadir ):
    print "ERROR!!! train data directory \""+traindatadir+"\" not found"
    return  
  if not os.path.exists( modelsdir ):
    os.makedirs( modelsdir )  
  if not os.path.exists( BASEDIR+"/temp/RR" ):
    os.makedirs( BASEDIR+"/temp/RR" )
  if not os.path.exists( BASEDIR+"/results" ):
    os.makedirs( BASEDIR+"/results" )
    
  trainLabel = BASEDIR+"/temp/RR/train_label"
  trainFeat = BASEDIR+"/temp/RR/train_feat"
  resultsdir = BASEDIR+"/results"
  

  label_list = []
  feat_list = []
  
  for ch in range(CHANNELS):
    if not os.path.exists( traindatadir+"/train_CH_"+str(ch+1)+".wer" ):
      print "ERROR!!! WER file "+ traindatadir+"/train_CH_"+str(ch+1)+".wer not found"
      return
    else:
      label_list.append( np.nan_to_num(np.genfromtxt( traindatadir+"/train_CH_"+str(ch+1)+".wer",delimiter=' ')) )
    if not os.path.exists( traindatadir+"/train_CH_"+str(ch+1)+"_"+FEAT+".feat" ):
      print "ERROR!!! Feature file "+ traindatadir+"/train_CH_"+str(ch+1)+"_"+FEAT+".feat not found"
      return
    else:
      feat_list.append( np.nan_to_num(np.genfromtxt( traindatadir+"/train_CH_"+str(ch+1)+"_"+FEAT+".feat",delimiter=' ')) )
  
  data_size = label_list[0].shape[0]
  feat_number = feat_list[0].shape[1]
  
  data_label = np.zeros([CHANNELS*data_size, 1])
  data_feat = np.zeros([CHANNELS*data_size, feat_number])
  for i in range(data_size):
    for ch in range(CHANNELS):
      data_label[i*CHANNELS+ch] = label_list[ch][i] 
      data_feat[i*CHANNELS+ch] = feat_list[ch][i]
      
  np.savetxt( trainLabel, data_label , fmt='%.3f') 
  np.savetxt( trainFeat, data_feat , fmt='%.4f') 

  import my_batch_et2
  my_batch_et2.main(trainLabel, trainFeat, modelsdir, 1, 10, 5)

  print "\nTest on Training set: "  
  import XRT_REG_test
  XRT_REG_test.main(trainFeat, trainLabel, modelsdir, resultsdir+"/train.pwer")
  print "Predicted WERs are stored in "+ resultsdir+"/train.pwer"  
  
    
if __name__=='__main__':
    sys.exit(main(sys.argv[1]), main(sys.argv[2]))


