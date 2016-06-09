#!/usr/bin/env python Prepare the words for LM feature extraction
from __future__ import division
import sys 
import os
import numpy as np

from __main__ import config


def main(setname, data_size):

  TMP = config['BASEDIR'] + "/temp/"

  print "    Extract WER scores for %s ..." % setname

  # define the transcription channels (training or test set)
  if setname == "train" :
    ref = config['trainREF']
    data_size = sum(1 for line in open(config['trainREF']))
    transcChannels = config['train_transcChannels'].strip().split()
  elif setname == "test" :
    ref = config['testREF']
    data_size = sum(1 for line in open(config['trainREF']))
    transcChannels = config['test_transcChannels'].strip().split()
  else :
    print "Error!!! Define the set name train or test\n"
    return

  CHANNELS = int(config['CHANNELS'])
  
  wer_matrix = np.zeros([data_size,CHANNELS])

  # for each transcription channels, compute the WER of each sentence
  for ch in range(CHANNELS):

    hyp = transcChannels[ch]
    out = config['BASEDIR'] + "/data/features/"+setname+"_CH_"+str(ch+1)+".wer"
    
    tmp_ref = open( TMP+"tmp_ref" , 'w')  
    tmp_hyp = open( TMP+"tmp_hyp" , 'w')
    
   
    with open(hyp) as f1, open(ref) as f2:
      for x,y in zip(f1,f2):
        if x.strip().split()[0] == y.strip().split()[0]:
          tmp_hyp.write( " ".join( x.strip().split()[1:] ) ) ; tmp_hyp.write( "\n" )  
          tmp_ref.write( " ".join( y.strip().split()[1:] ) ) ; tmp_ref.write( "\n" )         
        else:
          print "ERROR !!! in " + hyp + " " + x.strip().split()[0] + " id does not match " + y.strip().split()[0] + " id in ref...\n"
          return
   
    tmp_hyp.close()
    tmp_ref.close()
   
    # use levellnshtein distance to compute WERs
    Command = config['BINDIR']+"/bin/levenshtein " + TMP+"tmp_ref" + " " + TMP+"tmp_hyp" + " | head -n -1"
    os.system ( Command + " > " + TMP+"wer_output" )
  
    # save the WERs in the "out" file
    doc_out = open( out , 'w')
    doc_in = open ( TMP+"wer_output" )
    i = 0
    for line in doc_in:
      wer_matrix[i,ch] = float(line.strip().split()[-1].rstrip("%"))/100 
      doc_out.write( "%.3f\n" % wer_matrix[i,ch] )
      i += 1
    doc_in.close()
    doc_out.close()
  
  # also compute the rank of each transcription channel for each sentence
  import rank_array
  rank_matrix = rank_array.main(wer_matrix)
  
  np.savetxt( config['BASEDIR'] + "/data/features/"+setname+".rank", rank_matrix , fmt='%d') 
  
  for ch in range(CHANNELS):
    np.savetxt( config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch+1)+".rank", rank_matrix[:,[ch]] , fmt='%d')
    
    

if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))
  
  
  
  
  
  
