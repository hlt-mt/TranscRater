
#!/usr/bin/env python Prepare the words for LEX feature extraction
import os, sys

BINDIR = "/home/jalalvand/Downloads/TranscRater-master"
BASEDIR = "/home/jalalvand/Downloads/TranscRater-master"


#. $BINDIR/bin/control_libraries.sh
sys.path.insert(0, BINDIR+"/REG-QE")	
sys.path.insert(0, BINDIR+"/bin")	

CHANNELS = 5  # Since there are 5 transcription channels in the data files

train_size = 1000
test_size = 640

FEAT = "SIG_LEX"

if not os.path.exists( BASEDIR+"/temp" ):
  os.makedirs( BASEDIR+"/temp" )

RR_Iter = 10

import RR_train
RR_train.main( BASEDIR+"/data", BASEDIR+"/RR_models" )

import RR_test
RR_test.main( BASEDIR+"/data", BASEDIR+"/RR_models" )


