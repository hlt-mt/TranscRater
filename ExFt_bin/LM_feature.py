#!/usr/bin/env python extract features from LEXFEAT dictionary

from __future__ import division
from itertools import islice
import math
import time
import re
import numpy as np

from __main__ import config

# load the LM output file 
def load_lm_feat(ffile):
  doc=open(ffile, 'r')
  word2lm=[]
  for line in doc:
    word=line.strip().split()[0]
    lmf=line.strip().split()[1:]
    lmfn=[]
    for elem in lmf:
      lmfn.append(float(elem))
    word2lm.append([word,lmfn])    
  return word2lm
  


def main(setname, lm_feature_file):

  w2l = load_lm_feat(lm_feature_file);
  w2l_len = len(w2l)

  ch=0
  SUM = np.empty((0,len(w2l[0][1])), float)
  f = []
  
  # for each recognized words, extract the LM probabilities
  for i in range(w2l_len):
    if ( "transcrater_start_of_channel_" in w2l[i][0] ):
      ch+=1      
      f=open(config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch)+"_LM.feat",'w')    
    elif (w2l[i][0] == "</s>"):
      if ( SUM.size ):
        for elem in  np.mean(SUM,axis=0): # for each sentence, compute the mean of its word LM feature vectors
          f.write("%.4f " % elem)
          
        for j in range(len(w2l[0][1])):
          ind = SUM[:,j].ravel().nonzero()
          if ( len(ind[0]) > 0 ):
            f.write("%.4f " % np.sum( np.log10(SUM[ind[0],j])) )
          else:
            f.write("%.4f " % 0 )
        for j in range(len(w2l[0][1])):
          ind = SUM[:,j].ravel().nonzero()
          if ( len(ind[0]) > 0 ):
            f.write( "%.4f " % np.exp ( -np.sum(np.log10(SUM[ind[0],j])) / len(ind[0]) ) )
          else:
            f.write("%.4f " % 0 )
        f.write("\n")
        
      SUM = np.empty((0,len(w2l[0][1])), float)
    else:
      SUM=np.append(SUM, np.array([w2l[i][1]]), axis=0)
  f.close() 

if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))
  
  
