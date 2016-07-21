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
    
    ndcgat = "NDCG@"+config['CHANNELS']
    for bg in [10 ,50 ,100]:
        for tr in [5, 10, 20]:
            for lf in [5, 10, 20]:             
                parameters= '-ranker 8 -bag '+str(bg)+' -tree '+str(tr)+' -leaf '+str(lf) #+' -rtype 6'
                print parameters,
                args=[config['RANKLIBDIR']+"/RankLib-2.6.jar", "-train", trainfile,
                        parameters,
                        "-srate", "0.3", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" , "-mls", "10",
                        "-norm", "zscore", "-kcv", "5", "-metric2t", ndcgat, "-metric2T", ndcgat, " | grep Total | awk '{print $NF}' " ]
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
       
   best_parameters="-ranker 8 -bag 50 -tree 20 -leaf 10" # -rtype 6"

   # ----------------- Train/valid RR models

   if int(config['MLR_Tune']) :
       best_parameters= tune_MLR(config['RANKLIBDIR'], trainfile, config['folds'])
    
   print "\nTrain MLR models on \""+trainfile+"\" with best parameters of \""+best_parameters+"\" ..."

   trainData=trainfile 
  
   ndcgat = "NDCG@"+config['CHANNELS'] 
   args=[config['RANKLIBDIR']+"/RankLib-2.6.jar", "-train", trainData, best_parameters,
                "-srate", "0.3", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" ,
                "-norm", "zscore", "-mls" ,"10","-metric2t", ndcgat,
                "-save",modelsdir+"/MLR.model "]
   subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()


   # --------------- Test on Train
   import MLR_test
   MLR_test.main(trainfile ,modelsdir,config['BASEDIR']+"/temp/MLR/train.prank")




if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])
