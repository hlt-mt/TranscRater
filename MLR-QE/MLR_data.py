'''
Created on May 31, 2016

@author: qwaider
'''
import sys, getopt,os
from __main__ import *
from main import readJson
from itertools import izip


def main(argv):
     if len(sys.argv) < 0 :
        print 'MLR_data.py -n <name>'
        sys.exit(2)
     setname="train"
     CHANNELS=""
      
     try:
          opts, args = getopt.getopt(argv, "hn:", ["name="])
     except getopt.GetoptError:
          print 'MLR_data.py -n <name>'
          sys.exit(2)
     for opt, arg in opts:
          if opt == '-h':
             print 'MLR_data.py -n <name>'
             sys.exit()
          elif opt in ("-n", "--name"):
             setname = arg
          
     print "\nNAME \""+setname+"\"...\n"
     #readJson.main()
     setlist=[]
     if setname == 'train':
         train_transcChannels=readJson.config['train_transcChannels'].split(' ')
         setlist=train_transcChannels
     elif setname == "test":
         test_transcChannels=readJson.config['test_transcChannels'].split(' ')
         setlist=test_transcChannels
     else :
         print "\nERROR!!! Define a set name \"train\" or \"test\" for ./MLR-QE/MLR_data.py"
         sys.exit(2)
     # ---------------- Data Preparation
     f = open(readJson.config['BASEDIR']+"/data/MLR_${setname}_${Feat}.data",'w')
     for obj in range(len(setlist) ):
         #print obj,"=",setlist[obj]
         #TODO qid=${setlist[$(($segN-1))]}
         qid=obj
         for ch in range(len(CHANNELS) ):
             with open(readJson.config['BASEDIR']+"/data/features/${setname}_CH_${ch}.rank") as textfile1, open(readJson.config['BASEDIR']+"/data/features/${setname}_CH_${ch}_${Feat}.feat") as textfile2: 
                 for x, y in izip(textfile1, textfile2):
                     x = x.strip()
                     y = y.strip()
                     #print("{0}\t{1}".format(x, y))
                     #TODO sed -n "${segN}p"
                     line="{0} {1}".format(x, y)
                     line = line.replace(obj+"p","");
                     #awk -v "qid=$qid" '{printf("%d qid:%s",$1,qid) ; for(i=2;i<=NF;i++) printf(" %d:%.5f",i-1,$i); printf("\n")}';
                     line=x+" qid:"+qid
                     f.write(line+os.linesep)

     f.close()
  
          
     
      
      
      
      
   
if __name__ == "__main__":
   main(sys.argv)