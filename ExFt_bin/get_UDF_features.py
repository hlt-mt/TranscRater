#!/usr/bin/env python Prepare the words for LEX feature extraction
from __future__ import division
import sys 
import os
import numpy as np

from __main__ import *


def main(setname):

  # define the transcription channels (training or test set)
  if setname == "train" :
    data_size = sum(1 for line in open(config['trainREF']))
    transcChannels = config['train_transcChannels'].strip().split()
  elif setname == "test" :
    data_size = sum(1 for line in open(config['testREF']))
    transcChannels = config['test_transcChannels'].strip().split()
  else :
    print "Error!!! Define the set name train or test\n"
    return

  CHANNELS = int(config['CHANNELS'])
      
    
  # Control if the User Defined Feature file exists
  for ch in range(CHANNELS):
    udf_file = config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch+1)+"_UDF.feat"
    if  not os.path.isfile(udf_file):
      print "ERROR!!! User Defined Feature file %s does not exist" % udf_file
      return
    else:  
      udf_feat = np.nan_to_num(np.genfromtxt( udf_file, delimiter=' ') )
      
      # Control if the UDF file has the same number of instances as data size
      if udf_feat.shape[0] != data_size:
        print "ERROR!!! User defined feature %s does not match with data_size" % udf_file
        return
        
        
if __name__=='__main__':
  sys.exit(main(sys.argv[1]))  
