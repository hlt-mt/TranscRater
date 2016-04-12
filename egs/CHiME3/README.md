## CHiME3 example with 5 microphone

For this example, we use  data from the 3rd CHiME challenge (http://spandh.dcs.shef.ac.uk/chime_challenge/chime2015/data.html) which were collected for multiple distant microphone speech recognition in noisy environments.
CHiME-3 data consists of sentences of the Wall Street Journal corpus, uttered by four speakers in four noisy environments, and recorded by five frontal microphones placed on the frame of a tablet PC (a sixth one, placed on the back, mainly records background noise). 
Training and test respectively contain 1,640 and 1,320 sentences. 


### Fast Run
To run the toolkit fastly without using signal features (SIG), set the following variables in "./configuration1.conf" file:
```
BASEDIR= the full path of the directory of CHiME3 exsample on your computer.
BINDIR= the full path of the directory of "TranscRater" directory.
```
Then run the following command:
```
time . ../../bin/run-QE.sh configuration1.conf
```

Afterwards, change the QE=RR variable to QE=MLR and then run:
```
time . ../../bin/run-QE.sh configuration1.conf
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

- ./data/transcriptions/test_CH_1.txt
- ./data/transcriptions/test_CH_3.txt
- ./data/transcriptions/test_CH_4.txt
- ./data/transcriptions/test_CH_5.txt
- ./data/transcriptions/test_CH_6.txt


In order to use the signal based features, the user needs to download the audio data from (http://spandh.dcs.shef.ac.uk/chime_challenge/chime_download.html) and provides a list of the audio files (full path) in a file and put the name of this list in the corresponding field in the configuration file. 

To do so:
1. item click on the link above
2. download "CHiME3_isolated_dt05_real"
3. select "CHiME3_isolated_dt05_real.zip" option and click on download
4. unzip the file and save the path to this folder


Follow the same procedure to download the evaluation set by selecting "CHiME3_isolated_et05_real" and then "CHiME3_isolated_et05_real.zip". 
Again the transcriptions of these audio files by the baseline ASR systems are provided in "./data/transcriptions/test_CH_i.txt".


After downloading the audio files the user needs to prepare a list file for each microphone, in the same order as the reference files. 
For example, if the unzipped file is in 
```
CHDIR=/home/jalalvand/Downloads/CHiME3
```
then one can use the following bash command to make the audio list file for each microphone:
```
TranscRater> for Mic in 1 3 4 5 6; do
cat data/train.ref | cut -d" " -f1 | 
sed "s/_real//g" | tr "[:lower:]" "[:upper:]"|
while read id; do 
find ${CHDIR}/data/audio/16kHz/isolated/dt05_*/${id}.CH${Mic}.wav 
done > ./data/lists/train_CH_${Mic}.list
```

Note that we won't use the second microphone as it is placed on the back side of the tablet device and it mostly captures the noise.

The same command can be used for the evaluation set:
```
TranscRater> for Mic in 1 3 4 5 6; do
cat data/test.ref | cut -d" " -f1 | 
sed "s/_real//g" | tr "[:lower:]" "[:upper:]"|
while read id; do 
find ${CHDIR}/data/audio/16kHz/isolated/et05_*/${id}.CH${Mic}.wav 
done > ./data/lists/test_CH_${Mic}.list
```

