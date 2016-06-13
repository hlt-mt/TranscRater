'''
Created on May 31, 2016

@author: jalalvand
'''
import os, sys
import json


# include the commands directories
BINDIR = os.getcwd()
sys.path.insert(0, BINDIR+"/bin")
sys.path.insert(0, BINDIR+"/REG-QE")

# load config.json file
with open("config.json", 'r') as f:
   config = json.load(f)

# set variables
traindir  = config['BASEDIR']+"/data/features"
testdir   = config['BASEDIR']+"/data/features"
modelsdir = config['BASEDIR']+"/MLR_models"
out_file  = config['BASEDIR']+"/results/test.pwer"

# make folders
if not os.path.exists( config['BASEDIR']+"/temp" ):
  os.makedirs( config['BASEDIR']+"/temp" )
if not os.path.exists( config['BASEDIR']+"/results" ):
  os.makedirs( config['BASEDIR']+"/results" )

# train Regression models
import RR_train
RR_train.main( traindir, modelsdir )

# predict WERs
import RR_test
RR_test.main( testdir, modelsdir, out_file )


