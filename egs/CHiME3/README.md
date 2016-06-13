## CHiME3: An example with 5 microphone

For this example, we use  data from the 3rd CHiME challenge (http://spandh.dcs.shef.ac.uk/chime_challenge/chime2015/data.html) which were collected for multiple distant microphone speech recognition in noisy environments.
CHiME-3 data consists of sentences of the Wall Street Journal corpus, uttered by four speakers in four noisy environments, and recorded by five frontal microphones placed on the frame of a tablet PC (a sixth one, placed on the back, mainly records background noise). 
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

The "./data/" directory includes the references for for the training and test sets:
```
cat ./data/train.ref
cat ./data/test.ref
```

The transcriptions of the frontal microphones (1st, 3rd, 4th, 5th and 6th) using the baseline ASR system are also provided "./data/transcriptions/":

- ./data/transcriptions/train_CH_1.txt
- ./data/transcriptions/train_CH_3.txt
- ./data/transcriptions/train_CH_4.txt
- ./data/transcriptions/train_CH_5.txt
- ./data/transcriptions/train_CH_6.txt

and
- ./data/transcriptions/test_CH_1.txt
- ./data/transcriptions/test_CH_3.txt
- ./data/transcriptions/test_CH_4.txt
- ./data/transcriptions/test_CH_5.txt
- ./data/transcriptions/test_CH_6.txt


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

The same command can be used for the evaluation set:

Then run the following command:
```
~/TranscRater> python run-QE.py
```

### Using LEX features

### Using POS features

### Using LM features

### Using UDF features
