'''
Created on June 9, 2016

@author: jalalvand

this code extract the desired features (wrt config.json file) for
both train set and the test set.
The signals and transcriptions of the training/test sets must be defined 
in "config.json".

egs:
  python get_the_features.py "train"
'''

import sys
import numpy as np

from __main__ import config


def main ( setname ):

  # set data size
  if setname == "train":
    global data_size 
    data_size = sum(1 for line in open(config['trainREF']))
  else:
    global data_size 
    data_size = sum(1 for line in open(config['testREF']))
    
  CHANNELS = int(config['CHANNELS'])

  if not os.path.exists ( config['BASEDIR']+"/data/features" ):
    os.makedirs( config['BASEDIR']+"/data/features" )  
  

  # Compute WER scores and Ranks  
  import get_WER_scores
  get_WER_scores.main( setname , data_size )


  # Extract Signal features
  if "SIG" in config['FEAT']:
    import get_SIG_features
    get_SIG_features.main( setname )
      
  # Extract Lexical features
  if "LEX" in  config['FEAT']:
    import get_LEX_features
    get_LEX_features.main( setname )

  # Extract Language Model features
  if "LM" in config['FEAT']:
    import get_LM_features
    get_LM_features.main( setname )

  # Extract Part-of-Speech tag features
  if "POS" in config['FEAT']:
    import get_POS_features
    get_POS_features.main( setname )

  # Use the User Defined features
  if "UDF" in config['FEAT']:
    import get_UDF_features
    get_UDF_features.main( setname )
  #    ....

  
  # Accumulate the Extracted features for each Channel of transcription
  if '_' in config['FEAT']:  # if different types of features are asked
  
    for ch in range(CHANNELS):
    
      feat_array = np.array([])
      for feat in config['FEAT'].split('_'):
        tmparr = np.nan_to_num(np.genfromtxt("data/features/"+setname+"_CH_"+str(ch+1)+"_"+feat+".feat",delimiter=' '))
        if (feat_array.size == 0):
          feat_array = tmparr
        else:
          feat_array = np.column_stack ( [ feat_array , tmparr ] )
     
      np.savetxt( config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch+1)+"_"+config['FEAT']+".feat", feat_array , fmt='%.4f') 
    

if __name__=='__main__':
  sys.exit(main(sys.argv[1]))
      
  
    
    
  
  

