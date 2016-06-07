'''
Created on May 31, 2016

@author: qwaider
'''
import MLR_train
import readJson
import MLR_test
if __name__ == '__main__':
    
   # MLR_train.main(["-t" ,readJson.config['BASEDIR']+"/data/MLR_train_LEX_LM_POS.data" ,"-f" ,"10" ,"-m","MLR_models","-c","5"])
    MLR_test.main(["-t",readJson.config['BASEDIR']+"/data/MLR_test_LEX_LM_POS.data","-m","MLR_models","-o",readJson.config['BASEDIR']+"/data/MLR_output.prank","-c","5"])
pass