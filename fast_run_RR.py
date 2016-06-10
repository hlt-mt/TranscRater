
#!/usr/bin/env python Prepare the words for LEX feature extraction
#!/usr/bin/env python Prepare the words for LEX feature extraction
import os, sys
import json


# include the commands directories
BINDIR = os.getcwd()
sys.path.insert(0, BINDIR+"/bin")
sys.path.insert(0, BINDIR+"/REG-QE")

with open("config.json", 'r') as f:
   config = json.load(f)

traindir  = config['BASEDIR']+"/data/features"
testdir   = config['BASEDIR']+"/data/features"
modelsdir = config['BASEDIR']+"/MLR_models"
out_file  = config['BASEDIR']+"/results/test.pwer"


if not os.path.exists( config['BASEDIR']+"/temp" ):
  os.makedirs( config['BASEDIR']+"/temp" )
if not os.path.exists( config['BASEDIR']+"/results" ):
  os.makedirs( config['BASEDIR']+"/results" )


import RR_train
RR_train.main( traindir, modelsdir )

import RR_test
RR_test.main( testdir, modelsdir, out_file )


