'''
Created on May 31, 2016

@author: qwaider
'''
import sys, getopt,os
#from __main__ import *
from itertools import izip
from main import readJson


def main(argv):
     if len(sys.argv) < 0 :
        print 'MLR_data.py -n <name>'
        sys.exit(2)
     setname="train"
     Feat = "LEX"
     CHANNELS=readJson.config['train_transcChannels'].split(' ')
      
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
     setlist=list()
     if setname == 'train':
         file=readJson.config['train_transcChannels'].split(' ')[0]
         with open(file.strip(),'r') as fin:
          for line in fin:
              setlist.append((line.split(' ')[0]).strip())
              
     elif setname == "test":
         file=readJson.config['test_transcChannels'].split(' ')[0]
         with open(file.strip(),'r') as fin:
          for line in fin:
              setlist.append((line.split(' ')[0]).strip())
     else :
         print "\nERROR!!! Define a set name \"train\" or \"test\" for ./MLR-QE/MLR_data.py"
         sys.exit(2)
     # ---------------- Data Preparation
     f = open(readJson.config['BASEDIR']+"/data/MLR_"+setname+"_"+Feat+".data",'w+')
     for obj in range(len(setlist) ):
         #print obj,"=",setlist[obj]
         #TODO qid=${setlist[$(($segN-1))]}
         #print "line:"+str(obj)
         qid=setlist[obj]
         for ch in range(len(CHANNELS)):
             ind=ch+1
             #print "ch:"+str(ch)+" ind:"+str(ind)
             i=0
             from itertools import izip
             textfile1= open(readJson.config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ind)+".rank")
             textfile2= open(readJson.config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ind)+"_"+Feat+".feat") 
             for x, y in izip(textfile1, textfile2):
                     if(i==obj) :
                         x = x.strip()
                         y = y.strip()
                         w = y.split(' ')
                         stt=""
                         for wi in range(len(w)):
                             wind = wi+1
                             stt = stt+str(wind)+":"+w[wi]+" "
                             
                         line=x+" qid:"+qid+" "+stt
                         f.write(line+os.linesep)
                         
                     if i > obj :
                         break
                     i=i+1
             textfile1.close()
             textfile2.close()
     f.close()
  
          
     
      
      
      
      
   
if __name__ == "__main__":
   main(sys.argv)