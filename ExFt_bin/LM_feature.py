#!/usr/bin/env python

from __future__ import division
from sys import *
from itertools import islice
#from sets import Set
import math
import time
import re
import numpy as np



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
	
	
basedir = argv[1]
setname = argv[2]
lm_feature_file = argv[3]

if ( basedir == "" or setname == "" or lm_feature_file == ""):
        print "\nERROR!!! Wrong input to \"LM_feature.py\"\n"

w2l = load_lm_feat(lm_feature_file);
w2l_len = len(w2l)

ch=0
f=[]

SUM = np.empty((0,len(w2l[0][1])), float)

for i in range(w2l_len):
        if ( "transcrater_start_of_channel_" in w2l[i][0] ):
                if(f):
                        f.close()
                ch+=1
                f=open(basedir+"/data/features/"+setname+"_CH_"+str(ch)+"_LM.feat",'w')                
        elif (w2l[i][0] == "</s>"):
                if ( SUM.size ):
                        for elem in  np.mean(SUM,axis=0):
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




