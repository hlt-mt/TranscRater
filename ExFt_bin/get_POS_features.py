'''
Created on June 9, 2016

@author: jalalvand

this code runs a POS tagger on the transcriptions and extracts the related features.
the TreeTagger directory/model must be provided by the user.

egs:
  python get_POS_features.py "train"
'''

from __future__ import division
import sys 
import os
import numpy as np

from __main__ import config


def main(setname):

  TMP = config['BASEDIR'] + "/temp/"
  pos_file = TMP + setname + "_all_POS.txt"
  
  print "    Extract POS features for %s ..." % setname

  if not os.path.exist(config['TREETAGDIR'] + "/tree-tagger") :
    print "ERROR!!! in ExFt_bin/get_POS_features.py "
    print "         "+config['TREETAGDIR'] + "/tree-tagger "+" does not exist. You might need to download and compile it and then set its location in config.json"
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
  
  # In this file we write all the transcribed words by all the channels
  # one word per line. The channels are separated by "transcrater_start_of_channel_{ch}"
  doc_out = open( pos_file , 'w' )

  for ch in range(len(transcChannels)):
    transc = transcChannels[ch]
    doc_out.write ( "transcrater_start_of_channel_%s" % str(ch+1) )    
    doc_in = open(transc, 'r')
    for line in doc_in:
      for word_elem in line.strip().split():
        if word_elem == "<unk>":
          doc_out.write ("unknownword\n")
        else:
          doc_out.write("%s\n" % word_elem)
      doc_out.write( "#\n" )  
    doc_in.close()
  
  doc_out.close()
  
  # Run the TreeTagger on the transcribed files
  Command = "cat " + pos_file + " | " + config['TREETAGDIR'] + "/tree-tagger " + config['BINDIR'] + "/AUXFILE/english.par -quiet -token -lemma -sgml -prob -threshold 0.001 | awk '{print $1,$2,$4}'"
  os.system ( Command + " > " + TMP + setname + "_all_POS" )

  # Collect the POS features for each sentence   
  import POS_feature
  POS_feature.main (setname, TMP + setname + "_all_POS")


if __name__=='__main__':
    sys.exit(main(sys.argv[1]))

