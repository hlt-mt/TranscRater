'''
Created on June 9, 2016

@author: jalalvand

compute WER between two text files. Each line is identified by the ID of 
the sentence.

egs:
  python compute_WER.py  reference hypothesis
  
P.S. The core is written by Martin Thoma, https://martin-thoma.com/word-error-rate-calculation/#comment-2727808425
'''

from __future__ import division

import sys
import argparse
import math
import numpy as np
from itertools import izip
  
#!/usr/bin/env python

def main(ref, hyp):
    # initialisation
    WER_arr = np.array([])
    with open(ref,'r') as rf, open(hyp,'r') as hf:

        for rl,hl in izip(rf,hf):
                        
            if rl.strip().split()[0] == hl.strip().split()[0]:
                            
                r = rl.strip().split()[1:]
                h = hl.strip().split()[1:]
                    
                d = np.zeros((len(r)+1)*(len(h)+1), dtype=np.uint8)
                d = d.reshape((len(r)+1, len(h)+1))
                for i in range(len(r)+1):
                    for j in range(len(h)+1):
                        if i == 0:
                            d[0][j] = j
                        elif j == 0:
                            d[i][0] = i

                # computation
                for i in range(1, len(r)+1):
                    for j in range(1, len(h)+1):
                        if r[i-1] == h[j-1]:
                            d[i][j] = d[i-1][j-1]
                        else:
                            substitution = d[i-1][j-1] + 1
                            insertion    = d[i][j-1] + 1
                            deletion     = d[i-1][j] + 1
                            d[i][j] = min(substitution, insertion, deletion)

                WER_arr = np.append( WER_arr, (d[len(r)][len(h)] / len(r)) )
              
            else:
                print "ERROR!!! hyp id:"+rl.strip().split()[0]+" does not match with ref id:"+hl.strip().split()[0]
                print "HINT: You might need to reorder the transcriptions and the references to be compatible\n"
                return

    return WER_arr
            
if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2]))
