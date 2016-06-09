#!/usr/bin/env python

from __future__ import division
from itertools import islice
import math
import time
import re
import numpy as np

from __main__ import config

# load the computed POS features
def load_pos_feat(wordf):
  doc = open(wordf,'r')
  words = []
  for word in doc.read().split('\n'):
    words.append(word)  
  return words
  

def main(setname, pos_feature_file):

  w2p = load_pos_feat(pos_feature_file);
  w2p = filter(None, w2p)
  w2p_len = len(w2p)

  ch=0
  f=[]

  # [1-6] NUM NOU FUN VER ADJ ADV TOT
  pos1 = np.empty((0,3), float)
  pos2 = np.empty((0,7), float)

  # for each recognized word, extract the computed POS feature vector
  for i in range(w2p_len):
    word = w2p[i].split()

    if i > 0:
      pword = w2p[i-1].split()
    else:
      pword = w2p[i].split()  
    if i < w2p_len-1:
      nword = w2p[i+1].split()
    else:
      nword = w2p[i].split()
      
    
    if ( "transcrater_start_of_channel_" in word[0] ):
      if(f):
        f.close()
      ch+=1
      f=open(config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch)+"_POS.feat",'w')
      
    elif ( word[0] == '#' ):
      if ( pos1.size ):
        for elem in  np.mean(pos1,axis=0): # for each sentence, compute the mean of its word POS feature vectors
          f.write("%.4f " % elem)
        f.write("%.4f " % float(np.sum(pos2[:,0])) )
        f.write("%.4f " % float(np.sum(pos2[:,1]) / np.sum(pos2[:,0])) )
        f.write("%.4f " % float(np.sum(pos2[:,2]) / np.sum(pos2[:,0])) )
        f.write("%.4f " % float(np.sum(pos2[:,3]) / np.sum(pos2[:,0])) )
        f.write("%.4f " % float(np.sum(pos2[:,4]) / np.sum(pos2[:,0])) )
        f.write("%.4f " % float(np.sum([pos2[:,2], pos2[:,4], pos2[:,5], pos2[:,6]]) / np.sum(pos2[:,0])) )      
      f.write("\n")  
      
      pos1 = np.empty((0,3), float)
      pos2 = np.empty((0,7), float)  
      
    else:

      tmpArr = np.array( [ float(pword[2]), float(word[2]), float(nword[2]) ] )
      pos1 = np.vstack( [pos1, tmpArr] )
      
      
      if word[1] in ('CD' or 'CC'):
        pos2 =  np.vstack( [pos2, [1, 1, 0, 0, 0, 0, 0]] )
      elif word[1] in ('NN' or 'NNS' or 'NP' or 'NPS' or 'NAM' or 'NOM' or 'NPR' or 'PER' or 'NMON' or 'NMEA'): # if the word is NOUN
        pos2 =  np.vstack( [pos2, [1, 0, 1, 0, 0, 0, 0]] )
      elif word[1] in ('DT' or 'EX' or 'FW' or 'IN' or 'LS' or 'MD' or 'PDT' or 'POS' or 'PP' or 'RP' or 'TO' or 'WDT' or 'WP' or 'WP$' or 'WRB' or 'PP$' or 'UH' or 'SYM'): # if the word is CONTENT
        pos2 =  np.vstack( [pos2, [1, 0, 0, 1, 0, 0, 0]] )
      elif 'V' in word[1]: # if the word is VERB
        pos2 =  np.vstack( [pos2, [1, 0, 0, 0, 1, 0, 0]] )
      elif word[1] in ('JJ' or 'JJR' or 'JJS'): # if the word is ADJECTIVE
        pos2 =  np.vstack( [pos2, [1, 0, 0, 0, 0, 1, 0]] )
      else:
        pos2 =  np.vstack( [pos2, [1, 0, 0, 0, 0, 0, 1]] )
     
  f.close()
  
if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))
  
  
