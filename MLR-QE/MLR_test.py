'''
Created on May 31, 2016

@author: qwaider
'''
import sys, getopt, os
import readJson
import subprocess
def main(argv):
    if len(sys.argv) < 0 :
            print 'MLR_test.py -t <testfile> -o <outputfile> -m <modelsdir> -c <channels>'
            sys.exit(2)
      
    testFile = ''
    modelsdir = ''
    outfile = ''
    #CHANNELS = readJson.config['train_transcChannels'].split(' ')
    CHANNELS="5"
      
      
    try:
          opts, args = getopt.getopt(argv, "ht:o:m:c:", ["testfile=", "outputfile=", "modelsdir=","channel="])
    except getopt.GetoptError:
          print 'MLR_test.py -t <testfile> -o <outputfile> -m <modelsdir> -c <channels>'
          sys.exit(2)
    for opt, arg in opts:
          if opt == '-h':
             print 'MLR_test.py -t <testfile> -o <outputfile> -m <modelsdir> -c <channels>'
             sys.exit()
          elif opt in ("-t", "--testfile"):
             testFile = arg
          elif opt in ("-o", "--outputfile"):
             outfile = arg
          elif opt in ("-m", "--modelsdir"):
             modelsdir = arg
          elif opt in ("-c", "--channel"):
             CHANNELS = arg
    print "\nTest \"" + modelsdir + "\" on \"" + testFile + "\"...\n"
      # ----------------- Predict ranks
      # cat $testFile | cut -d' ' -f 1 > $BASEDIR/temp/MLR/test.label
    mkdir_p(readJson.config['BASEDIR'] + "/temp/MLR/")
    f = open(readJson.config['BASEDIR'] + "/temp/MLR/test.label", 'w')
    with open(testFile, 'r') as fin:
          for line in fin:
              line = line.split(' ')[0]
              f.write(line + os.linesep)
    f.close()
    args = [readJson.config['RANKLIBDIR'] + "/RankLib-2.6.jar", "-load", modelsdir + "/MLR.model", "-rank", testFile, "-norm", "zscore", "-metric2T", "NDCG@"+CHANNELS, "-score", readJson.config['BASEDIR'] + "/temp/MLR/Scores"]  # TODO  2>&1 | grep WriteNothing
    print subprocess.Popen('java -jar' + (''.join(list(str(" " + e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()
    f = open(outfile, 'w')
    with open(readJson.config['BASEDIR'] + "/temp/MLR/Scores", 'r') as fin:
          for line in fin:  
              line = "{0:.3f}".format(float(line.split('\t')[2]))  # TODO awk '{printf("%.3f\n", $NF)}' 
              f.write(line + os.linesep)
    f.close()
      # ----------------- Compute NDCG
    args = [readJson.config['BINDIR'] + "/bin/rank_array.py", readJson.config['BASEDIR'] + "/temp/MLR/test.label", CHANNELS, readJson.config['BASEDIR'] + "/temp/MLR/test.label.rank"]
    print subprocess.Popen('python' + (''.join(list(str(" " + e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()
    args = [readJson.config['BINDIR'] + "/bin/rank_array.py", outfile, CHANNELS, outfile + ".rank"]  # TODO ${outfile}.rank
    print subprocess.Popen('python' + (''.join(list(str(" " + e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()
    args = [readJson.config['BINDIR'] + "/bin/compute_NDCG.py", readJson.config['BASEDIR'] + "/temp/MLR/test.label.rank", outfile + ".rank"]  # TODO ${outfile}.rank
    print subprocess.Popen('python' + (''.join(list(str(" " + e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()

from subprocess import *

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

