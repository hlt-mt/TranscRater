'''
Created on May 30, 2016

@author: qwaider
'''

import sys, getopt
from main import MLR_test, readJson

def main(argv):
   if len(sys.argv) < 0 :
      print 'MLR_train.py -t <trainFile> -f <folds> -m <modelsdir>'
      sys.exit(2)
   
   trainfile = ''
   folds = ''
   modelsdir = ''
   best_parameters="-ranker 8 -bag 50 -tree 20 -leaf 10"
   
   try:
      opts, args = getopt.getopt(argv,"ht:f:m:",["tfile=","folds=","modelsdir="])
   except getopt.GetoptError:
      print 'MLR_train.py -t <trainFile> -f <folds> -m <modelsdir>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'MLR_train.py -t <trainFile> -f <folds> -m <modelsdir>'
         sys.exit()
      elif opt in ("-t", "--tfile"):
         trainfile = arg
      elif opt in ("-f", "--folds"):
         folds = arg
      elif opt in ("-m", "--modelsdir"):
         modelsdir = arg
   print 'Train file is: ', trainfile
   print 'Folds is: ', folds
   print 'ModelsDir is: ', modelsdir
   # ----------------- Train/valid RR models
   #mkdir -p $modelsdir
   mkdir_p(modelsdir)
   if readJson.config['MLR_Tune'] == "Yes":
       tune_MLR(readJson.config['RANKLIBDIR'],trainfile,folds)
    
   print "\nTrain MLR models on \""+trainfile+"\" with best parameters of \""+best_parameters+"\" ..."
   trainData=trainfile #$BASEDIR/temp/folds/shuffled_train.data
   
   args=[readJson.config['RANKLIBDIR']+"/RankLib-2.6.jar","-train",trainData,best_parameters,"-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5" ,"-tc" ,"1" ,"-mls" ,"10","-norm zscore" ,"-metric2t", "NDCG@${CHANNELS}" ,"-save",modelsdir+"/MLR.model"] #TODO  2>&1 | grep WriteNothing
   result = jarWrapper(*args)
   print "done\n"                            

    # --------------- Test on Train

    #. $BINDIR/MLR-QE/MLR_test.sh $trainFile $modelsdir $BASEDIR/temp/MLR/train.prank
   MLR_test.main([trainfile ,modelsdir,readJson.config['BASEDIR']+"/temp/MLR/train.prank"])





def tune_MLR(RANKLIBDIR,trainfile,folds):
    print 'MLR parameter tuning ...'
    bg = [10 ,50 ,100]
    tr = [5, 10, 20]
    lf = [5, 10, 20]
    for bgi in range(len(bg) ):
        for tri in range(len(tr)):
            for lfi in range(len(lf)):
                print '%sranker %d %sbag %d %stree %d %sleaf %d  - ',type ,' - ',bg[bgi],' - ',tr[tri],' - ',lf[lfi] #TODO
                result = call_java(RANKLIBDIR,trainfile,type,bg,tr,lf,folds)
                print result
                # > $BASEDIR/temp/MLR/train.log
                best_parameters='cat $BASEDIR/temp/MLR/train.log | sort -n -k 9 -r | head -n 1 | cut -d\' \' -f-8'  
                
import errno    
import os
def call_java(RANKLIBDIR,trainFile,type,bg,tr,lf,folds):
     args = [ RANKLIBDIR+"/RankLib-2.6.jar", "-train", trainFile, "-ranker", type, "-bag", bg, "-tree", tr, "-leaf", lf, "-srate", "0.1", "-frate", "0.5", "-shrinkage", "0.5", "-tc", "1", "-mls", "10","-kcv", folds, "-norm", "zscore",  "-metric2t", "NDCG@${CHANNELS} -metric2T NDCG@${CHANNELS}" ]#TODO  2>&1 | grep \"Total\" | awk '{print $NF}'  " ] # Any number of args to be passed to the jar file
     result = jarWrapper(*args)
     return result    
    
from subprocess import *

def jarWrapper(*args):
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
    ret = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith('\n'):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')
    return ret
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
