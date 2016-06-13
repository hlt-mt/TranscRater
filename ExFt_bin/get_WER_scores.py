#!/usr/bin/env python Prepare the words for LM feature extraction
from __future__ import division
import sys 
import os
import numpy as np

from __main__ import config


def main(setname):

  TMP = config['BASEDIR'] + "/temp/"

  print "    Extract WER scores for %s ..." % setname

  # define the transcription channels (training or test set)
  data_size = 0
  if setname == "train" :
    ref = config['trainREF']
    data_size = sum(1 for line in open(config['trainREF']))
    transcChannels = config['train_transcChannels'].strip().split()
  elif setname == "test" :
    ref = config['testREF']
    data_size = sum(1 for line in open(config['testREF']))
    transcChannels = config['test_transcChannels'].strip().split()
  else :
    print "Error!!! Define the set name train or test\n"
    return

  CHANNELS = int(config['CHANNELS'])
  

  # for each transcription channels, compute the WER of each sentence
  wer_matrix = np.zeros([data_size,CHANNELS])
  for ch in range(CHANNELS):

    hyp = transcChannels[ch]
    out = config['BASEDIR'] + "/data/features/"+setname+"_CH_"+str(ch+1)+".wer"

    # use levellnshtein distance to compute WERs  
    import compute_WER
    WER = compute_WER.main(ref,hyp)
    np.savetxt( out , WER , fmt='%.3f')   
    wer_matrix[:,ch] = WER
  
  # also compute the rank of each transcription channel for each sentence
  import rank_array
  rank_matrix = rank_array.main(wer_matrix)
  
  np.savetxt( config['BASEDIR'] + "/data/features/"+setname+".rank", rank_matrix , fmt='%d') 
  
  for ch in range(CHANNELS):
    np.savetxt( config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch+1)+".rank", rank_matrix[:,[ch]] , fmt='%d')
    
    

if __name__=='__main__':
  sys.exit(main(sys.argv[1]))
  
  
  
  
  
  
