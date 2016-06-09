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
    bg = [10 ,50 ,100]
    tr = [5, 10, 20]
    lf = [5, 10, 20]
    f = open(config['BASEDIR']+"/temp/MLR/train.log",'w+')

    for bgi in range(len(bg) ):
        for tri in range(len(tr)):
            for lfi in range(len(lf)):
                line= '-ranker '+str(type)+' -bag '+str(bg[bgi])+' -tree '+str(tr[tri])+' -leaf '+str(lf[lfi])+' '
                f.write(line+os.linesep)
                args = [ RANKLIBDIR+"/RankLib-2.6.jar", "-train", trainfile, "-ranker", type, 
                         "-bag", bg, "-tree", tr, "-leaf", lf, "-srate", "0.1", "-frate", "0.5", 
                         "-shrinkage", "0.5", "-tc", "1", "-mls", "10","-kcv", folds, "-norm", 
                         "zscore",  "-metric2t", "NDCG@${CHANNELS} -metric2T NDCG@${CHANNELS}" ]
                subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()
                f.write(line+os.linesep)
                
                
    f.close()
    
    best_parameters='cat $BASEDIR/temp/MLR/train.log | sort -n -k 9 -r | head -n 1 | cut -d\' \' -f-8'  
                    
        
        
def main(trainfile, modelsdir):

   if not os.path.exists( config['BASEDIR']+"/temp" ):
       os.makedirs( config['BASEDIR']+"/temp" )
   if not os.path.exists( config['BASEDIR']+"/temp/MLR" ):
       os.makedirs( config['BASEDIR']+"/temp/MLR" )
       
   best_parameters="-ranker 8 -bag 50 -tree 20 -leaf 10"

   # ----------------- Train/valid RR models

   if config['MLR_Tune'] == "Yes":
       tune_MLR(config['RANKLIBDIR'],trainfile,folds)
    
   print "\nTrain MLR models on \""+trainfile+"\" with best parameters of \""+best_parameters+"\" ..."

   trainData=trainfile 
   
   args=[config['RANKLIBDIR']+"/RankLib-2.6.jar","-train",trainData,best_parameters,
                "-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" ,
                "-mls" ,"10","-norm zscore" ,"-metric2t", "NDCG@"+config['CHANNELS'] ,
                "-save",modelsdir+"/MLR.model 2>&1 | grep WriteNothing"]
   subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()


   # --------------- Test on Train
   import MLR_test
   MLR_test.main(trainfile ,modelsdir,config['BASEDIR']+"/temp/MLR/train.prank")




if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])
