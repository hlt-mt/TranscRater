
#!/usr/bin/env python Prepare the words for LEX feature extraction
#!/usr/bin/env python Prepare the words for LEX feature extraction
import os, sys
import json


# include the commands directories
BINDIR = "/home/jalalvand/Downloads/TranscRater-master"
sys.path.insert(0, BINDIR+"/bin")
sys.path.insert(0, BINDIR+"/REG-QE")

with open("config.json", 'r') as f:
   config = json.load(f)

train_file  = config['BASEDIR']+"/data/MLR_train_"+config['FEAT']+".data"
test_file   = config['BASEDIR']+"/data/MLR_test_"+config['FEAT']+".data"
models      = config['BASEDIR']+"/MLR_models"
output_file = config['BASEDIR']+"/resutls/test.pred"


if not os.path.exists( config['BASEDIR']+"/temp" ):
  os.makedirs( config['BASEDIR']+"/temp" )



import RR_train
RR_train.main( config['BASEDIR']+"/data", config['BASEDIR']+"/RR_models" )

import RR_test
RR_test.main( config['BASEDIR']+"/data", config['BASEDIR']+"/RR_models" )


