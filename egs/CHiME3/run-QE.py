'''
Created on June 9, 2016

@author: jalalvand

this is a wrapper to load the cofiguration ("config.json"), 
extract the features, train the models and test the models

egs:
  python run-QE.py
'''
import os, sys
import json


# include the commands directories
BINDIR = "/home/jalalvand/Desktop/TranscRater"
sys.path.insert(0, BINDIR+"/bin")
sys.path.insert(0, BINDIR+"/ExFt_bin")
sys.path.insert(0, BINDIR+"/REG-QE")
sys.path.insert(0, BINDIR+"/MLR-QE")

# load the configuration file into "config"
with open("config.json", 'r') as f:
   config = json.load(f)


# make the necessary directories
if not os.path.exists( config['BASEDIR']+"/temp" ):
  os.makedirs( config['BASEDIR']+"/temp" )
if not os.path.exists( config['BASEDIR']+"/results" ):
  os.makedirs( config['BASEDIR']+"/results" )


# extract the features
print "\nPerform Feature Selection..."
import get_the_features
get_the_features.main("train")
get_the_features.main("test")


# train regression models
print "\nWER predction process..."
import RR_train
RR_train.main( config['BASEDIR']+"/data/features", config['BASEDIR']+"/RR_models" )

# predict the WER
import RR_test
RR_test.main( config['BASEDIR']+"/data/features", config['BASEDIR']+"/RR_models", config['BASEDIR']+"/results/test.pwer" )




# prepare the train data
print "\nRANK predction process..."
import MLR_data
MLR_data.main("train")

# train the MLR model
import MLR_train
MLR_train.main(config['BASEDIR']+"/data/MLR_train_"+config['FEAT']+".data", config['BASEDIR']+"/MLR_models")


# prepare the test data
import MLR_data
MLR_data.main("test")

# predict the ranks
import MLR_test
MLR_test.main( config['BASEDIR']+"/data/MLR_test_"+config['FEAT']+".data", config['BASEDIR']+"/MLR_models", config['BASEDIR']+"/results/test.prank" )

