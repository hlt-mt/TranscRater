'''
Created on June 9, 2016

@author: jalalvand

this code runs different language models (RNNLMs and SRILMs) if they are 
provided by the user and extract the related features.

egs:
  python get_LM_features.py "train"
'''

from __future__ import division
import sys 
import os
import numpy as np

from __main__ import config


def main(setname):

  TMP = config['BASEDIR'] + "/temp"

  print "    Extract LM features for %s ..." % setname

  # define the transcription channels (training or test set)
  if setname == "train" :
    transcChannels = config['train_transcChannels'].strip().split()
  elif setname == "test" :
    transcChannels = config['test_transcChannels'].strip().split()
  else :
    print "Error!!! Define the set name train or test\n"
    return

  CHANNELS = int(config['CHANNELS'])
  
  # In the first file, we write all the transcription sentences by all the channels
  # In the second file, we write all the transcribed words per line
  doc_out1 = open( TMP + "/" + setname + "_all_LM.txt", 'w' )
  doc_out2 = open( TMP + "/" + setname + "_all_words.txt", 'w' )

  for ch in range(len(transcChannels)):
    transc = transcChannels[ch]
    doc_out1.write ( "transcrater_start_of_channel_" + str(ch+1) + '\n' )
    doc_out2.write ( "transcrater_start_of_channel_" + str(ch+1) + "\n</s>\n" )    
    doc_in = open(transc, 'r')
    for line in doc_in:
      doc_out1.write( " ".join( line.strip().split()[1:] ) ) ; doc_out1.write( "\n" )  
      doc_out2.write( "\n".join( line.strip().split()[1:] ) ) ; doc_out2.write( "\n</s>\n" )  
    doc_in.close()
  
  doc_out1.close()
  doc_out2.close()  
    


  flag=0

  tmplmfeat=""

  # Run the trained Language Models on the transcriptions.
  # Up to 4 LMs are available:
  #   (general-domain RNN, in-domain RNN, general-domain 4grLM and in-domain 4grLM
  if (config['RNNLM1']):
    print "      Extract LM features by " + config['RNNLM1'] + "..."
    Command = config['RNNLMDIR'] + "/rnnlm -rnnlm " + config['RNNLM1'] + " -test " + TMP + "/" + setname + "_all_LM.txt  -debug 2 | sed -n '6,$p' | head -n -4 | awk '{print $2}'" 
    os.system(Command + " > " + TMP+"/"+setname+"_all.rnn1")
    flag=1
    tmplmfeat += " " + TMP+"/"+setname+"_all.rnn1"


  if (config['RNNLM2']):
    print "      Extract LM features by " + config['RNNLM2'] + "..."
    Command = config['RNNLMDIR'] + "/rnnlm -rnnlm " + config['RNNLM2'] + " -test " + TMP + "/" + setname + "_all_LM.txt  -debug 2 | sed -n '6,$p' | head -n -4 | awk '{print $2}'" 
    os.system(Command + " > " + TMP+"/"+setname+"_all.rnn2")
    flag=1
    tmplmfeat += " " + TMP+"/"+setname+"_all.rnn2"


  if (config['SRILM1']):
    print "      Extract LM features by " + config['SRILM1'] + "..."
    Command =  config['SRILMDIR'] + "/ngram  -lm " + config['SRILM1'] + " -order 4 -ppl " + TMP + "/" + setname + "_all_LM.txt -debug 2 2>&1 | grep \"\[\" | cut -d'=' -f2 | awk '{print $2}'"
    os.system(Command + " > " + TMP+"/"+setname+"_all.sri1")
    flag=1
    tmplmfeat += " " + TMP + "/" + setname + "_all.sri1"


  if (config['SRILM2']):
    print "      Extract LM features by " + config['SRILM2'] + "..."
    Command =  config['SRILMDIR'] + "/ngram  -lm " + config['SRILM2'] + " -order 4 -ppl " + TMP + "/" + setname + "_all_LM.txt -debug 2 2>&1 | grep \"\[\" | cut -d'=' -f2 | awk '{print $2}'"
    os.system(Command + " > " + TMP+"/"+setname+"_all.sri2")
    flag=1
    tmplmfeat += " " + TMP + "/" + setname + "_all.sri2"


  # Collect the word based LM features in a single file
  Command  = "paste " + TMP + "/" + setname + "_all_words.txt " + tmplmfeat
  os.system ( Command + " | tr '\t' ' ' > " + TMP + "/" + setname + "_all.lm" )

  # Compute the LM features for each sentence  
  import LM_feature
  LM_feature.main (setname, TMP + "/" + setname + "_all.lm")



if __name__=='__main__':
    sys.exit(main(sys.argv[1]))

