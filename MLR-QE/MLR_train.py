'''
Created on May 30, 2016

@author: qwaider
'''

import sys, getopt
import os
from __main__ import config
import subprocess
import errno    


def tune_MLR(RANKLIBDIR,trainfile,folds):
    print 'MLR parameter tuning ...'
    
    log = []
    
    for bg in [10 ,50 ,100]:
        for tr in [5, 10, 20]:
            for lf in [5, 10, 20]:             
                parameters= '-ranker 8 -bag '+str(bg)+' -tree '+str(tr)+' -leaf '+str(lf)+' -rtype 6'
                print parameters,
                args=[config['RANKLIBDIR']+"/RankLib-2.6.jar", "-train", trainfile,
                        parameters,
                        "-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" , "-mls", "10",
                        "-kcv", "5", "-norm zscore -metric2t NDCG@10 -metric2T NDCG@10 | grep Total | awk '{print $NF}' " ]
                proc = subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE)
                partial_ndcg = proc.stdout.read()
                log.append((parameters, partial_ndcg))
                print partial_ndcg
                    
    best_parameters = sorted(log, key=lambda log: log[1],reverse=True)[0][0]
    print "best found parameters: %s" % best_parameters    
    return  best_parameters


def main(trainfile, modelsdir):

   if not os.path.exists( config['BASEDIR']+"/temp" ):
       os.makedirs( config['BASEDIR']+"/temp" )
   if not os.path.exists( config['BASEDIR']+"/temp/MLR" ):
       os.makedirs( config['BASEDIR']+"/temp/MLR" )
       
   best_parameters="-ranker 8 -bag 50 -tree 20 -leaf 10"

   # ----------------- Train/valid RR models

   if int(config['MLR_Tune']) :
       best_parameters= tune_MLR(config['RANKLIBDIR'], trainfile, config['folds'])
    
   print "\nTrain MLR models on \""+trainfile+"\" with best parameters of \""+best_parameters+"\" ..."

   trainData=trainfile 
   
   args=[config['RANKLIBDIR']+"/RankLib-2.6.jar", "-train", trainData, best_parameters,
                "-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" ,
                "-mls" ,"10","-norm zscore" ,"-metric2t", "NDCG@"+config['CHANNELS'] ,
                "-save",modelsdir+"/MLR.model 2>&1 | grep WriteNothing"]
   subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()


   # --------------- Test on Train
   import MLR_test
   MLR_test.main(trainfile ,modelsdir,config['BASEDIR']+"/temp/MLR/train.prank")




if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])
