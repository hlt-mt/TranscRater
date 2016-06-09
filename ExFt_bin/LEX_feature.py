#!/usr/bin/env python extract features from LEXFEAT dictionary

from __future__ import division
from itertools import islice
import math
import time
import re
import numpy as np

from __main__ import config

# laod the predefined LEXical features
def load_features(ffile):
  doc=open(ffile, 'r')
  word2f={}
  for line in doc:
    features=[]
    word=line.strip().split()[0]
    for f in line.strip().split()[1:]:
            features.append(int(f))
    
    if not word2f.has_key(word):
      word2f[word] = features; 
  return word2f;

# load the words
def load_words(wordf):
        doc = open(wordf,'r')
        words = []
        for word in doc.read().split():
                words.append(word)  
        return words
        
        
def main(setname, words_file):

  w2f =   load_features(config['LEXFEAT']);
  words = load_words(words_file)

  featsize = len(w2f.items()[0][1])

  ch=0
  f=[]

  SUM = np.empty((0, featsize),  float)
  
  # for each recognized word, extract its lexical feature vector
  for w in words:     
    if ( "transcrater_start_of_channel_" in w ):
      if(f):
        f.close()
      ch+=1
      f=open(config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch)+"_LEX.feat",'w')
      SUM = np.empty((0, featsize), float)
    elif ( w == '#' ):
      if ( SUM.size ):
        for elem in  np.mean(SUM, axis=0):  # for each sentence, compute the mean of its word lexical feature vector
          f.write("%.4f " % elem)
        f.write("\n")
        SUM = np.empty((0, featsize), float)
    else:  
      if ( w2f.get(w) ):
        SUM = np.vstack( [ SUM, w2f.get(w) ] )
      else:
        SUM = np.vstack( [ SUM, np.zeros((1, featsize) , float) ] )

  f.close()

if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))
