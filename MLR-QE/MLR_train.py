'''
Created on May 30, 2016

@author: qwaider
'''

import sys, getopt
import MLR_test, readJson
import subprocess

def main(argv):
   if len(sys.argv) < 0 :
      print 'MLR_train.py -t <trainFile> -f <folds> -m <modelsdir> -c <channels>'
      sys.exit(2)
   
   trainfile = ''#output of MLR_data
   folds = '5'#ex5
   modelsdir = ''#a directory to output
   best_parameters="-ranker 8 -bag 50 -tree 20 -leaf 10"
   CHANNELS="5"
   try:
      opts, args = getopt.getopt(argv,"ht:f:m:c:",["tfile=","folds=","modelsdir=","channel="])
   except getopt.GetoptError:
      print 'MLR_train.py -t <trainFile> -f <folds> -m <modelsdir> -c <channels>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'MLR_train.py -t <trainFile> -f <folds> -m <modelsdir> -c <channels>'
         sys.exit()
      elif opt in ("-t", "--tfile"):
         trainfile = arg
      elif opt in ("-f", "--folds"):
         folds = arg
      elif opt in ("-m", "--modelsdir"):
         modelsdir = arg
      elif opt in ("-c", "--channel"):
         CHANNELS = arg
   print 'Train file is: ', trainfile
   print 'Folds is: ', folds
   print 'ModelsDir is: ', modelsdir
   print 'Channels is: ', CHANNELS

   # ----------------- Train/valid RR models
   #mkdir -p $modelsdir
   mkdir_p(modelsdir)
   if readJson.config['MLR_Tune'] == "Yes":
       tune_MLR(readJson.config['RANKLIBDIR'],trainfile,folds)
    
   print "\nTrain MLR models on \""+trainfile+"\" with best parameters of \""+best_parameters+"\" ..."
   trainData=trainfile #$BASEDIR/temp/folds/shuffled_train.data
   
   args=[readJson.config['RANKLIBDIR']+"/RankLib-2.6.jar","-train",trainData,best_parameters,"-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" ,"-mls" ,"10","-norm zscore" ,"-metric2t", "NDCG@"+str(CHANNELS) ,"-save",modelsdir+"/MLR.model"] #TODO  2>&1 | grep WriteNothing
   #print os.popen('java -jar '+(''.join(list(str(" "+e) for e in args)))).read()
   #print('java -jar'+(''.join(list(str(" "+e) for e in args))))
   print subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()

   print "done\n"                            

    # --------------- Test on Train

   MLR_test.main([trainfile ,modelsdir,readJson.config['BASEDIR']+"/temp/MLR/train.prank"])





def tune_MLR(RANKLIBDIR,trainfile,folds):
    print 'MLR parameter tuning ...'
    bg = [10 ,50 ,100]
    tr = [5, 10, 20]
    lf = [5, 10, 20]
    f = open(readJson.config['BASEDIR']+"/temp/MLR/train.log",'w+')

    for bgi in range(len(bg) ):
        for tri in range(len(tr)):
            for lfi in range(len(lf)):
                line= '-ranker '+str(type)+' -bag '+str(bg[bgi])+' -tree '+str(tr[tri])+' -leaf '+str(lf[lfi])+' '
                f.write(line+os.linesep)
                args = [ RANKLIBDIR+"/RankLib-2.6.jar", "-train", trainfile, "-ranker", type, "-bag", bg, "-tree", tr, "-leaf", lf, "-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5", "-tc", "1", "-mls", "10","-kcv", folds, "-norm", "zscore",  "-metric2t", "NDCG@${CHANNELS} -metric2T NDCG@${CHANNELS}" ]#TODO  2>&1 | grep \"Total\" | awk '{print $NF}'  " ] # Any number of args to be passed to the jar file
                print subprocess.Popen('java -jar'+(''.join(list(str(" "+e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()
                f.write(line+os.linesep)
                
                
    f.close()
    #
    best_parameters='cat $BASEDIR/temp/MLR/train.log | sort -n -k 9 -r | head -n 1 | cut -d\' \' -f-8'  
                
import errno    
import os
from subprocess import *


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
        
if __name__ == "__main__":
   main(sys.argv)
