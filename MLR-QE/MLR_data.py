'''
Created on May 31, 2016

@author: qwaider
'''
import sys, getopt,os
from itertools import izip
from __main__ import config


def main(setname):

     if not os.path.exists( config['RANKLIBDIR']+"/RankLib-2.6.jar" ):
         print "ERROR!!! RankLib is not ready in "+config['RANKLIBDIR']+"/RankLib-2.6.jar"
         return
     if not os.path.exists( config['BASEDIR']+"/temp" ):
         os.makedirs( config['BASEDIR']+"/temp" )
     if not os.path.exists( config['BASEDIR']+"/temp/MLR" ):
         os.makedirs( config['BASEDIR']+"/temp/MLR" )

     CHANNELS=0 
     setlist=list()

     if setname == 'train':
         CHANNELS=config['train_transcChannels'].split(' ')
         trfile=config['trainREF']
         with open(config['BASEDIR']+"/"+trfile.strip(),'r') as fin:
           for line in fin:
              setlist.append(line.strip().split(' ')[0])
              
     elif setname == "test":
         CHANNELS=config['test_transcChannels'].split(' ')
         trfile = config['testREF']
         with open(config['BASEDIR']+"/"+trfile.strip(),'r') as fin:
           for line in fin:
              setlist.append(line.strip().split(' ')[0])
     else :
         print "\nERROR!!! Define a set name \"train\" or \"test\" for "+config['BASEDIR']+"/MLR-QE/MLR_data.py"
         sys.exit(2)


     Feat = config['FEAT']

          
     print "\nPrepare data for \""+setname+"\"..."

     # ---------------- Data Preparation
     f = open(config['BASEDIR']+"/data/MLR_"+setname+"_"+Feat+".data",'w+')
     for obj in range(len(setlist) ):
         qid=setlist[obj]
         for ch in range(len(CHANNELS)):
             ind=ch+1
             i=0
             from itertools import izip
             textfile1= open(config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ind)+".rank")
             textfile2= open(config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ind)+"_"+Feat+".feat") 
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
   main(sys.argv[1])
