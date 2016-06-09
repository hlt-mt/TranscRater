'''
Created on June 9, 2016

@author: jalalvand

this code extracts the Lexicon features. The LEX features are previously 
computed for all the English words in the domain.

egs:
  python get_LEX_features.py "train"
'''

from __future__ import division
import sys 
import os
import numpy as np

from __main__ import config


def main(setname):

  TMP = config['BASEDIR'] + "/temp"

  print "    Extract Lexical features for %s ..." % setname

  if  not os.path.isfile(config['LEXFEAT']):
    print "ERROR!!! Lexicon Dictionary Feature file not found in LEXFEAT=\"%s\"\n" % config['LEXFEAT']
    return

  # define the transcription channels (training or test set)
  if setname == "train" :
    transcChannels = config['train_transcChannels'].strip().split()
  elif setname == "test" :
    transcChannels = config['test_transcChannels'].strip().split()
  else :
    print "Error!!! Define the set name train or test\n"
    return

  CHANNELS = int(config['CHANNELS'])
  
  # In this file we put all the transcriptions of all the channels separated by 
  # one line of "transcrater_start_of_channel_{ch}" 
  # the format is as one word per line and ending the sentence by '#'
  doc_out = open( TMP+"/"+setname+"_all_LEX.txt" , 'w')

  for ch in range(len(transcChannels)):
    transc = transcChannels[ch]
    doc_out.write("transcrater_start_of_channel_"+str(ch+1)+"\n")
    doc_in = open(transc, 'r')
    for line in doc_in:
      for w in line.strip().split()[1:]:
        doc_out.write(w+"\n")
      doc_out.write("#\n")
    doc_in.close()
  
  doc_out.close()

  # Look at LEXFEAT dictionary and find the feature vector for each word
  import LEX_feature
  LEX_feature.main (setname, config['BASEDIR']+"/temp/"+setname+"_all_LEX.txt")


if __name__=='__main__':
    sys.exit(main(sys.argv[1]))




