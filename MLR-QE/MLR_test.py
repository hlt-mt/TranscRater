'''
Created on May 31, 2016

@author: qwaider
'''
from __future__ import division
import sys, getopt, os
from __main__ import config
import subprocess
import numpy as np
import errno    

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise   
   

def main(testFile,modelsdir,outfile):
         
  
    print "\nTest \"" + modelsdir + "\" on \"" + testFile + "\"..."
    
    data_size = num_lines = sum(1 for line in open(testFile))

    # load the labels
    labels = np.array([])
    with open(testFile, 'r') as fin:
          for line in fin:
              labels = np.append (labels, int(line.split(' ')[0]))
    labels_rank_mat = labels.reshape([labels.shape[0]/int(config['CHANNELS']), int(config['CHANNELS'])])
    
    # predict the ranks
    args = [config['RANKLIBDIR']+"/RankLib-2.6.jar", "-load", modelsdir+"/MLR.model",
            "-rank", testFile, "-norm", "zscore", "-metric2T", "NDCG@"+config['CHANNELS'],
            "-score", config['BASEDIR'] + "/temp/MLR/Scores 2>&1 | grep WriteNothing"]
    subprocess.Popen('java -jar' + (''.join(list(str(" " + e) for e in args))), shell=True, stdout=subprocess.PIPE).stdout.read()

    # load the predicted scores into a matrix
    scores = np.array([])
    with open(config['BASEDIR'] + "/temp/MLR/Scores", 'r') as fin:
          for line in fin:  
               scores = np.append( scores, "{0:.3f}".format(float(line.split('\t')[2])) ) 
    scores_mat = scores.reshape([scores.shape[0]/int(config['CHANNELS']), int(config['CHANNELS'])]).astype(np.float)

    import rank_array
    pred_rank_mat = rank_array.main(scores_mat)

    np.savetxt( outfile, pred_rank_mat, fmt='%d') 
     
    # ----------------- Compute NDCG
    import compute_NDCG
    compute_NDCG.main ( labels_rank_mat, pred_rank_mat )
    
    
if __name__ == "__main__":
   main(sys.argv[1],sys.argv[2],sys.argv[3])

