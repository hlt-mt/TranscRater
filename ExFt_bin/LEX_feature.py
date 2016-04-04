#!/usr/bin/env python

from __future__ import division
from sys import *
from itertools import islice
import math
import time
import re
import numpy as np


def load_features(ffile):
	doc=open(ffile, 'r')
	word2f={}
	for line in doc:
		features=[]
		word=line.strip().split()[0]
		for f in line.strip().split()[1:]:
		        features.append(int(f))
		
		if not word2f.has_key(word):
			word2f[word] = features; #line.strip().split()[1:];
	return word2f;

def load_words(wordf):
        doc = open(wordf,'r')
        words = []
        for word in doc.read().split():
                words.append(word)	
        return words
        
	
basedir = argv[1]
setname = argv[2]
features_file = argv[3]
words_file	= argv[4]

if ( basedir == "" or setname == "" or features_file == "" or words_file == "" ):
        print "\nERROR!!! Wrong input to \"LEX_feature.py\"\n"


w2f =   load_features(features_file);
words = load_words(words_file)

featsize = len(w2f.items()[0][1])

ch=0
f=[]

SUM = np.empty((0, featsize),  float)

for w in words:     
        if ( "transcrater_start_of_channel_" in w ):
                if(f):
                        f.close()
                ch+=1
                f=open(basedir+"/data/features/"+setname+"_CH_"+str(ch)+"_LEX.feat",'w')
                SUM = np.empty((0, featsize), float)
        elif ( w == '#' ):
		if ( SUM.size ):
                        for elem in  np.mean(SUM,axis=0):
                                f.write("%.4f " % elem)
			f.write("\n")
        	SUM = np.empty((0, featsize), float)
	else:  
	        if ( w2f.get(w) ):
	                SUM = np.vstack( [ SUM, w2f.get(w) ] )
                else:
                        SUM = np.vstack( [ SUM, np.zeros((1, featsize) , float) ] )

f.close()


