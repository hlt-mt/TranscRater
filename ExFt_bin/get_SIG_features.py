'''
Created on June 9, 2016

@author: jalalvand

this code uses the CTM format of the transcription and
extract the related features from the signal.

egs:
  python get_SIG_features.py "train"
'''

from __future__ import division
import sys 
import os
import math
from decimal import Decimal
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav

import numpy as np

from __main__ import config

# laod the ctm files (words, times)
def load_ctm (ctmf):
  old_ind = ""
  ctm_id = []
  tmp = []
  doc_in = open(ctmf, 'r')
  for line in doc_in:
    new_ind, digit, t1, l, word = line.strip().split()
    if not new_ind == old_ind:
      old_ind = new_ind
      if len(tmp) > 0:
        ctm_id.append(tmp)
        tmp = []
    tmp.append([new_ind, digit, t1, l, word])
  if len(tmp) > 0:
    ctm_id.append(tmp)
  doc_in.close()
  return ctm_id

# assign the frames of each word to that word
# for the gaps, insert @bg as silence
def load_ctm_info (ctmf, fbank_feat):
  data = []
  t = 0
  t1=0
  l =0
  for line in ctmf:
    word = line[4]
    t1 = int( 100*Decimal(line[2]))
    l  = int( 100*Decimal(line[3]))
    if not t1 == t:
      if t1>t:
        frames=[]
        frames.append("@bg")
        frames.append(t)
        frames.append(t1)
        frames.append( fbank_feat[t:t1,:].mean() )
        data.append(frames)
      t = t1
    frames=[]
    frames.append(word)
    frames.append(t1)
    frames.append(t1+l)
    frames.append( fbank_feat[t1:t1+l,:].mean() )
    data.append(frames)
    t = t1 + l
  if not t == len(fbank_feat):
    frames=[]
    frames.append("@bg")
    frames.append(t)
    frames.append(len(fbank_feat))
    frames.append( fbank_feat[t:len(fbank_feat),:].mean() )
    data.append(frames)
  return data
  
  
  
def main(setname):

  print "    Extract SIG features for ", setname, " ..."

  if setname == "train" :
    waveChannels = config['train_waveChannels'].strip().split()
    transcChannels = config['train_transcChannels_ctm'].strip().split()
  elif setname == "test" :
    waveChannels = config['test_waveChannels'].strip().split()
    transcChannels = config['test_transcChannels_ctm'].strip().split()
  else :
    print "Error!!! Define the set name train or test\n"
    return

  CHANNELS = int(config['CHANNELS'])
  

  for ch in range(CHANNELS):
    
    print "      Extract SIG features for CHANNEL ", str(ch+1)

    # load the wave files for each recording channel
    wavfiles = "data/lists/"+setname+"_CH_"+str(ch+1)+"_wav.list"
    if not waveChannels[ch] or not transcChannels[ch]:
      print "ERROR!!! SIG features need .CTM format of transcriptions"
      return
    wavfiles = waveChannels[ch]
    ctmfile  = transcChannels[ch]

    # save the SIG features into this file
    sig_feat_file = config['BASEDIR']+"/data/features/"+setname+"_CH_"+str(ch+1)+"_SIG.feat"
  
    ctm_array = load_ctm (ctmfile)
    
    ind = -1
    feat_matrix = np.array([])

    wav_doc = open(wavfiles, 'r')

    # for each wave file, compute the frame mfcc/energy. then assign the frames to the recognized words
    for wavfile in wav_doc:

      ind += 1

      (rate,sig) = wav.read(wavfile.strip())
      mfcc_feat = mfcc(sig,rate,winlen=0.02,winstep=0.01,numcep=12)
      fbank_feat =logfbank(sig,rate,winlen=0.02,winstep=0.01, nfilt=1)
  
      w2fr = load_ctm_info (ctm_array[ind], fbank_feat)
    
      sil_no = 0; sil_e = 0; min_sil_e = 1000; max_sil_e = -1000; sil_dur = 0; std_sil_dur = 0
      wrd_no = 0; wrd_e= 0; min_wrd_e = 1000; max_wrd_e = -1000; wrd_dur = 0; std_wrd_dur = 0
  
      for elem in w2fr:
        w = elem[0]
        t1= elem[1]
        t2= elem[2]
        e = elem[3]
        if w == "@bg":  # if it's noise
          sil_no += 1
          sil_e += e
          sil_dur += t2-t1+1
          if e < min_sil_e:
            min_sil_e = e
          elif e > max_sil_e:
            max_sil_e = e      
        else :          # if it's word
          wrd_no += 1
          wrd_e += e
          wrd_dur += t2-t1+1
          if e < min_wrd_e:
            min_wrd_e = e
          elif e > max_wrd_e:
            max_wrd_e = e


      # compute the following Features   
      feat_vector = np.array([])
    
      feat_vector = np.append(feat_vector, mfcc_feat.shape[0]/100 ); # total seg duration
  
      feat_vector = np.append(feat_vector, mfcc_feat.mean (axis = 0) )  # mean of mfcc
  
      feat_vector = np.append(feat_vector, fbank_feat.mean (axis = 0) ) # mean of energy
      feat_vector = np.append(feat_vector, fbank_feat.min (axis = 0) ) # min of energy
      feat_vector = np.append(feat_vector, fbank_feat.max (axis = 0) ) # max of energy

      feat_vector = np.append(feat_vector, (sil_e/sil_no) ) # mean noise energy
      feat_vector = np.append(feat_vector, min_sil_e )  # min of noise energy
      feat_vector = np.append(feat_vector, max_sil_e )  # max of noise energy
  
      feat_vector = np.append(feat_vector, (wrd_e/wrd_no) )  # mean of word energies
      feat_vector = np.append(feat_vector, min_wrd_e )  # min of word energies
      feat_vector = np.append(feat_vector, max_wrd_e )  # max of noise energies
  
      feat_vector = np.append(feat_vector, (wrd_e/wrd_no) / (sil_e/sil_no) ) # Signal to Noise ratio
    
      feat_vector = np.append(feat_vector, max_wrd_e - min_sil_e ) # max word energy - min noise energy
   
      feat_vector = np.append(feat_vector, sil_no ) # number of silences
   
      feat_vector = np.append(feat_vector, sil_no / wrd_no ) # silence to noise ratio
  
      feat_vector = np.append(feat_vector, wrd_no / wrd_dur ) # number of words per second (frame)
  
      feat_vector = np.append(feat_vector, sil_no / sil_dur )  # number of silences per second (frame)
  
      feat_vector = np.append(feat_vector, wrd_dur )  # total words duration
  
      feat_vector = np.append(feat_vector, sil_dur )  # total silence duration
  
      feat_vector = np.append(feat_vector, wrd_dur / wrd_no )  # mean of words duration
  
      feat_vector = np.append(feat_vector, sil_dur / sil_no ) # mean of silence duration
  
      feat_vector = np.append(feat_vector, sil_dur / wrd_dur ) # silence to word duration ratio
  
      feat_vector = np.append(feat_vector, wrd_dur - sil_dur ) # word duration - silence duration

      for elem in w2fr:
        w = elem[0]
        t1= elem[1]
        t2= elem[2]
        if w == "@bg":  # if it's noise
          std_sil_dur += math.pow((t2-t1+1) - (sil_dur/sil_no) , 2)
        else:           # if it's word
          std_wrd_dur += math.pow((t2-t1+1) - (wrd_dur/wrd_no), 2 )
       
  
      feat_vector = np.append(feat_vector, math.sqrt ( std_wrd_dur ) / wrd_no ) # std of the words duration
   
      feat_vector = np.append(feat_vector, math.sqrt ( std_sil_dur ) / wrd_no )  # std of the silence duration
    
      if len(feat_matrix) < 1:
        feat_matrix = feat_vector
      else:
        feat_matrix = np.vstack([ feat_matrix, feat_vector] )

    np.savetxt( sig_feat_file, feat_matrix , fmt='%.4f')
  
  
if __name__=='__main__':
  sys.exit(main(sys.argv[1]))
  
