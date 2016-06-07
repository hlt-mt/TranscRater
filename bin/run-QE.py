#!/usr/bin/env python Runs the feature extraction and then the learning steps
# egs:
# python run-QE.py

import sys
import numpy as np


from __main__ import *

CHANNELS = 5
BASEDIR = "/home/jalalvand/Downloads/TranscRater-master/egs/CHiME3"
BINDIR = "/home/jalalvand/Downloads/TranscRater-master"

OPENSMILEDIR = "/home/jalalvand/Desktop/toolkits/signal_feature_tools/opensmile-2.0-rc1/opensmile"  # Set if you wanna use signal features
RNNLMDIR = "/home/jalalvand/Desktop/rnnlm/rnnlm-0.3e"   # set if you have the RNNLM models
SRILMDIR = "/home/jalalvand/Desktop/srilm/bin/i686-m64" # set if you wanna use SRILM
TREETAGDIR = "/home/jalalvand/Desktop/fbk_functions/TreeTagger/bin" # set if you wanna use POS features
RANKLIBDIR = "/home/jalalvand/Downloads"  # set if you wanna use machine learned ranking (MLR) models


RNNLM1 = "~/Desktop/ASR-QE-toolkit/egs/CHiME3/lm/rnnlm11M"
RNNLM2 = "~/Desktop/ASR-QE-toolkit/egs/CHiME3/lm/rnnlm1M"
SRILM1 = "~/Desktop/ASR-QE-toolkit/egs/CHiME3/lm/srilm37M_4gr.blm"
SRILM2 = "~/Desktop/ASR-QE-toolkit/egs/CHiME3/lm/srilm1M_4gr.blm"
LEXFEAT = BINDIR + "/AUXFILE/LexicalFeatures.txt"

trainREF = BASEDIR + "/data/train.ref"
testREF = BASEDIR + "/data/test.ref"


train_waveChannels=[]
for ch in range(CHANNELS):
  train_waveChannels.append(BASEDIR+"/data/lists/train_CH_"+str(ch+1)+"_wav.list")

test_waveChannels=[]
for ch in range(CHANNELS):
  test_waveChannels.append(BASEDIR+"/data/lists/test_CH_"+str(ch+1)+"_wav.list")


train_transcChannels=[]
for ch in range(CHANNELS):
  train_transcChannels.append(BASEDIR+"/data/transcriptions/train_CH_"+str(ch+1)+".txt")

test_transcChannels=[]
for ch in range(CHANNELS):
  test_transcChannels.append(BASEDIR+"/data/transcriptions/test_CH_"+str(ch+1)+".txt")


train_transcChannels_ctm=[]
for ch in range(CHANNELS):
  train_transcChannels_ctm.append(BASEDIR+"/data/transcriptions/train_CH_"+str(ch+1)+".ctm")

test_transcChannels_ctm=[]
for ch in range(CHANNELS):
  test_transcChannels_ctm.append(BASEDIR+"/data/transcriptions/test_CH_"+str(ch+1)+".ctm")


FEAT = "SIG_LEX"

RR_Iter = 10
folds = 5

sys.path.insert(0, BASEDIR)
sys.path.insert(0, BINDIR+"/bin")
sys.path.insert(0, BINDIR+"/ExFt_bin")
sys.path.insert(0, BINDIR+"/REG-QE")
sys.path.insert(0, BINDIR+"/MLR-QE")


# Extract features for train 
import get_the_features
get_the_features.main("train")

# Train RR models
import RR_train
RR_train.main(BINDIR+"data/features", "models/")


# Extract features for test
#import get_the_features
#get_the_features.main("test")

# Test the RR models
#import RR_test
#RR_test.main("models/")
  

