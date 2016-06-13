'''
Created on May 31, 2016

@author: qwaider
'''

#!/usr/bin/env python Prepare the words for LEX feature extraction
import os, sys
import json


# include the commands directories
BINDIR = os.getcwd()  
sys.path.insert(0, BINDIR+"/bin")
sys.path.insert(0, BINDIR+"/MLR-QE")


# load config.json file
with open("config.json", 'r') as f:
   config = json.load(f)

# set variables
train_file  = config['BASEDIR']+"/data/MLR_train_"+config['FEAT']+".data"
test_file   = config['BASEDIR']+"/data/MLR_test_"+config['FEAT']+".data"
models      = config['BASEDIR']+"/MLR_models"
output_file = config['BASEDIR']+"/results/test.pred"

# make folders
if not os.path.exists( config['BASEDIR']+"/temp" ):
  os.makedirs( config['BASEDIR']+"/temp" )
if not os.path.exists( config['BASEDIR']+"/results" ):
  os.makedirs( config['BASEDIR']+"/results" )



# prepare the train data
import MLR_data
MLR_data.main("train")

# train the MLR model
import MLR_train
MLR_train.main(train_file, models)


# prepare the test data
import MLR_data
MLR_data.main("test")

# predict the ranks
import MLR_test
MLR_test.main( test_file, models, output_file )

