#!/usr/bin/env python

from __future__ import division
from itertools import islice

from sys import *
import math
import time
import re
import numpy as np



#def load_pos_feat(ffile):
#	doc=open(ffile, 'r')
#	word2pos=[]
#	for line in doc:
#		word=line.strip().split()[0]
#		posf=line.strip().split()[1:]
#		posfn=[]
#		for elem in posf:
#		        posfn.append(float(elem))
#		word2pos.append([word,posfn])	
#	return word2pos
	
def load_pos_feat(wordf):
        doc = open(wordf,'r')
        words = []
        for word in doc.read().split('\n'):
                words.append(word)	
        return words
	

basedir = argv[1]
setname = argv[2]
pos_feature_file = argv[3]

if ( basedir == "" or setname == "" or pos_feature_file == ""):
        print "\nERROR!!! Wrong input to \"POS_feature.py\"\n"


w2p = load_pos_feat(pos_feature_file);
w2p = filter(None, w2p)
w2p_len = len(w2p)

ch=0
f=[]

# [1-6] NUM NOU FUN VER ADJ ADV TOT
pos1 = np.empty((0,3), float)
pos2 = np.empty((0,7), float)


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
                f=open(basedir+"/data/features/"+setname+"_CH_"+str(ch)+"_POS.feat",'w')
                
        elif ( word[0] == '#' ):
		if ( pos1.size ):
                        for elem in  np.mean(pos1,axis=0):
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
	        elif word[1] in ('NN' or 'NNS' or 'NP' or 'NPS' or 'NAM' or 'NOM' or 'NPR' or 'PER' or 'NMON' or 'NMEA'):
	                pos2 =  np.vstack( [pos2, [1, 0, 1, 0, 0, 0, 0]] )
	        elif word[1] in ('DT' or 'EX' or 'FW' or 'IN' or 'LS' or 'MD' or 'PDT' or 'POS' or 'PP' or 'RP' or 'TO' or 'WDT' or 'WP' or 'WP$' or 'WRB' or 'PP$' or 'UH' or 'SYM'):
	                pos2 =  np.vstack( [pos2, [1, 0, 0, 1, 0, 0, 0]] )
	        elif 'V' in word[1]:
	                pos2 =  np.vstack( [pos2, [1, 0, 0, 0, 1, 0, 0]] )
	        elif word[1] in ('JJ' or 'JJR' or 'JJS'):
	                pos2 =  np.vstack( [pos2, [1, 0, 0, 0, 0, 1, 0]] )
	        else:
	                pos2 =  np.vstack( [pos2, [1, 0, 0, 0, 0, 0, 1]] )
	 
f.close()
