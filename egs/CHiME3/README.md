## CHiME3: An example with 5 microphone

For this example, we use  data from the 3rd CHiME challenge (http://spandh.dcs.shef.ac.uk/chime_challenge/chime2015/data.html) which is collected for multiple distant microphone speech recognition in noisy environments.
CHiME-3 data consists of sentences of the Wall Street Journal corpus, uttered by four speakers in four noisy environments, and recorded by five frontal microphones placed on the frame of a tablet PC (a sixth one, placed on the back that mainly records the background noise). 
Training and test respectively contain 1,640 and 1,320 sentences. 


### Fast Run
To run the toolkit fastly without using signal features (SIG), set the following variables in "config.json" file:
```
BASEDIR= the full path of the directory of CHiME3 exsample on your computer.
BINDIR= the full path of the directory of "TranscRater" directory.
SRILMDIR= the full path of the directory of SRILM
TREETAGDIR= the full path of the directory of TREETAGGER
RANKLIBDIR= the full path of the directory of RankLib-2.6.jar
```
Then run the following command:
```
python run-QE.sh 
```

## Descriptions

The "./data/" directory includes the references for the training and test sets:
```
cat ./data/train.ref
cat ./data/test.ref
```

The transcriptions of the frontal microphones (1st, 2nd, 3rd, 4th and 5th) using the baseline ASR system are also provided "./data/transcriptions/":

- ./data/transcriptions/train_CH_1.txt
- ./data/transcriptions/train_CH_2.txt
- ./data/transcriptions/train_CH_3.txt
- ./data/transcriptions/train_CH_4.txt
- ./data/transcriptions/train_CH_5.txt

and
- ./data/transcriptions/test_CH_1.txt
- ./data/transcriptions/test_CH_2.txt
- ./data/transcriptions/test_CH_3.txt
- ./data/transcriptions/test_CH_4.txt
- ./data/transcriptions/test_CH_5.txt


### Using SIG features

The signal features need for .ctm format of the transcription. Therefore the user needs to provide them in "./data/transcription/" folder.

Also the user needs to download the audio data from (http://spandh.dcs.shef.ac.uk/chime_challenge/chime_download.html) and provides a list of the audio files (full path) in a file and put the name of this list in the corresponding field in the configuration file. 

To do so:
1. item click on the link above
2. download "CHiME3_isolated_dt05_real"
3. select "CHiME3_isolated_dt05_real.zip" option and click on download
4. unzip the file and save the path to this folder


Follow the same procedure to download the evaluation set by selecting "CHiME3_isolated_et05_real" and then "CHiME3_isolated_et05_real.zip". 
Again the transcriptions of these audio files by the baseline ASR systems are provided in "./data/transcriptions/test_CH_i.txt".

After downloading the signals, you need to provide a list of the signals for each channel in "./data/lists/" directory like the provided examples.

#### Note that the order of the files in the lists must match the order of the references.

Then run the following command:
```
~/TranscRater> python run-QE.py
```

### Using LEX features
LEXicon-based features are extracted using a lexical feature dictionary (optionally pro-vided by the user) in "AUXFILE/LexicalFeatures.txt". In this dictionary, to each individual word, a feature  vector  (containing the frequency of fricatives, liquids, nasals, stops and vowels in its pronunciation) is assigned.  Other elements of the vector are the number of homophones (words  with  the  same  pronunciation)  and  quasi-homophones (words with similar pronunciation).

The current "AUXFILE/LexicalFeatures.txt" file contains 315K english words. The words that are not included in this set will be considered as unkown word receinveing all zero vector. 

"ExFt_bin/get_LEX_features.py" prepares the transcriptions and extracts the features for each word.
"ExFt_bin/LEX_feature.py" collects the features and computes the mean of the values per sentence.

### Using LM features
Language  Model  features  include the  mean  of  word  probabilities,  the  sum  of  the log probabilities and the perplexity score for each transcription.  TranscRater allows using up to four different language models:  two RNNLMs trained on generic and specific data and two n-gramLM trained on generic and  specific  data. To  work  with  neural  network LMs, the tool makes use of RNNLM, while for n-gram LMs it uses SRILM toolkit.

We suggest the users to train the language models with regard to their tasks. 

"ExFt_bin/get_LM_features.py" prepares the transcriptions and run the language models to compute the probabilities the scores.
"ExFt_bin/LM_feature.py" collects the word level probabilities and computes the mean of the values per sentence.

### Using POS features
Part-Of-Speech features are extracted using the TreeTagger. For each word in the transcription, they consider the score assigned to the predicted POS of the word itself, the previous and the  following  one. 
"ExFt_bin/get_POS_features.py" prepares the transcriptions and run the TreeTagger to extract the scores.
"ExFt_bin/POS_feature.py" collects the features and computes the mean of the values per sentence.

### Using UDF features
User Defined Features are other features that the user may optionally add to the system. The format of the files must be like a feature file per sentence in a txt file. 
"ExFt_bin/get_UDF_features.py" simply control the user defined features if the size and the number of lines match the training and test sizes


