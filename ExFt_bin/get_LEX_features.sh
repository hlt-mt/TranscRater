#!/bin/bash Extract word features

setname=$1


TMP=$BASEDIR/temp

printf "    Extract Lexical features for $setname..."

if [[ ! -e $LEXFEAT ]]; then
  printf "ERROR!!! Lexicon Dictionary Feature file not found in LEXFEAT=\"$LEXFEAT\"\n"
  return
fi



if [[ $setname = "train" ]]; then
  transcChannels=(${train_transcChannels[*]})
elif [[ $setname = "test" ]]; then
  transcChannels=(${test_transcChannels[*]})
else
  printf "Error!!! Define the set name train or test\n"
  return
fi



for ch in $(seq 1 $CHANNELS)
do
  printf "transcrater_start_of_channel_$ch\n"
  cat ${transcChannels[$((ch-1))]} | cut -d' ' -f2- | sed 's/<unk>/kioonia/g' | sed 's/$/ #/g' | tr ' ' '\n'
done > $TMP/${setname}_all_LEX.txt


python $BINDIR/ExFt_bin/LEX_feature.py $BASEDIR $setname $LEXFEAT $BASEDIR/temp/${setname}_all_LEX.txt

printf "done\n"
