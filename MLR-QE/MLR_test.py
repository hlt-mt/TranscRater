'''
Created on May 31, 2016

@author: qwaider
'''
import sys, getopt,os
from main import readJson
def main(argv):
     if len(sys.argv) < 0 :
      print 'MLR_test.py -t <testfile> -o <outputfile> -m <modelsdir>'
      sys.exit(2)
      
      testFile=''
      modelsdir=''
      outfile=''
      CHANNELS=''
      
      
      try:
          opts, args = getopt.getopt(argv, "ht:o:m:", ["testfile=", "outputfile=", "modelsdir="])
      except getopt.GetoptError:
          print 'MLR_test.py -t <testfile> -o <outputfile> -m <modelsdir>'
          sys.exit(2)
      for opt, arg in opts:
          if opt == '-h':
             print 'MLR_test.py -t <testfile> -o <outputfile> -m <modelsdir>'
             sys.exit()
          elif opt in ("-t", "--testfile"):
             testFile = arg
          elif opt in ("-o", "--outputfile"):
             outfile = arg
          elif opt in ("-m", "--modelsdir"):
             modelsdir = arg
      print "\nTest \""+modelsdir+"\" on \""+testFile+"\"...\n"
      # ----------------- Predict ranks
      #cat $testFile | cut -d' ' -f 1 > $BASEDIR/temp/MLR/test.label
      f = open(readJson.config['BASEDIR']+"/temp/MLR/test.label",'w')
      with open(testFile,'r') as fin:
          for line in fin:
              line = line.split(' ')[0]
              f.write(line+os.linesep)
      f.close()
      args=[readJson.config['RANKLIBDIR']+"/RankLib-2.6.jar","-load",modelsdir+"/MLR.model","-rank",testFile,"-norm","zscore","-metric2T","NDCG@${CHANNELS}","-score",readJson.config['BASEDIR']+"/temp/MLR/Scores"] #TODO  2>&1 | grep WriteNothing
      result = jarWrapper(*args)
      f = open(outfile,'w')
      with open(readJson.config['BASEDIR']+"/temp/MLR/Scores",'r') as fin:
          for line in fin:  
              line = "{0:.3f}".format(float(line))   #TODO awk '{printf("%.3f\n", $NF)}' 
              f.write(line+os.linesep)
      f.close()
      # ----------------- Compute NDCG
      args=[readJson.config['BINDIR']+"/bin/rank_array.py",readJson.config['BASEDIR']+"/temp/MLR/test.label",CHANNELS,readJson.config['BASEDIR']+"/temp/MLR/test.label.rank"]
      result = pythonWrapper(*args)
      args=[readJson.config['BINDIR']+"/bin/rank_array.py",outfile,CHANNELS,outfile+".rank"] #TODO ${outfile}.rank
      result = pythonWrapper(*args)
      args=[readJson.config['BINDIR']+"/bin/compute_NDCG.py",readJson.config['BASEDIR']+"/temp/MLR/test.label.rank",outfile+".rank"] #TODO ${outfile}.rank
      result = pythonWrapper(*args)

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
def pythonWrapper(*args):
    process = Popen(['python']+list(args), stdout=PIPE, stderr=PIPE)
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


       
       
   
   
   
   
   
if __name__ == "__main__":
   main(sys.argv)

