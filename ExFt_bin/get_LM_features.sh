#!/bin/bash get LM features


setname=$1


TMP=$BASEDIR/temp

printf "    Extract LM features for $setname...\n"


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
  cat ${transcChannels[$((ch-1))]} | cut -d' ' -f2- 
done > $TMP/${setname}_all_LM.txt

cat $TMP/${setname}_all_LM.txt | awk '{print $L,"</s>"}' | sed "s/^ *//;s/ *$//;s/ \\{1,\\}/ /g" | tr ' ' '\n' > $TMP/${setname}_all.words

flag=0

tmplmfeat=""

if [[ -e $RNNLM1 ]]; then
  printf "      Extract LM features by $(basename $RNNLM1)..."
  if [[ ! -e $RNNLMDIR ]]; then
    printf "Error!!! RNNLM library not found in $RNNLMDIR\n"
  else
    $RNNLMDIR/rnnlm  -rnnlm $RNNLM1 -test $TMP/${setname}_all_LM.txt  -debug 2 | sed -n '6,$p' | head -n -4 | awk '{print $2}' > $TMP/${setname}_all.rnn1 
    printf "done\n" 
    flag=1
    tmplmfeat="$tmplmfeat $TMP/${setname}_all.rnn1"
  fi
fi

if [[ -e $RNNLM2 ]]; then
  printf "      Extract LM features by $(basename $RNNLM2)..."
  if [[ ! -e $RNNLMDIR ]]; then
    printf "Error!!! RNNLM library not found in $RNNLMDIR\n"
  else
    $RNNLMDIR/rnnlm  -rnnlm $RNNLM2 -test $TMP/${setname}_all_LM.txt  -debug 2 | sed -n '6,$p' | head -n -4 | awk '{print $2}'    > $TMP/${setname}_all.rnn2
    printf "done\n"
    flag=1
    tmplmfeat="$tmplmfeat $TMP/${setname}_all.rnn2"
  fi
fi

if [[ -e $SRILM1 ]]; then
  printf "      Extract LM features by $(basename $SRILM1)..."
  if [[ ! -e $SRILMDIR ]]; then
    printf "Error!!! SRILM library not found in $SRILMDIR\n"
  else
    $SRILMDIR/ngram  -lm $SRILM1 -order 4 -ppl $TMP/${setname}_all_LM.txt -debug 2 2>&1 | grep "\[" | cut -d'=' -f2 | awk '{print $2}' > $TMP/${setname}_all.sri1
    printf "done\n"
    flag=1
    tmplmfeat="$tmplmfeat $TMP/${setname}_all.sri1"
  fi
fi

if [[ -e $SRILM2 ]]; then
  printf "      Extract LM features by $(basename $SRILM2)..."
  if [[ ! -e $SRILMDIR ]]; then
    printf "Error!!! SRILM library not found in $SRILMDIR\n"
  else
    $SRILMDIR/ngram  -lm $SRILM2 -order 4 -ppl $TMP/${setname}_all_LM.txt -debug 2 2>&1 | grep "\[" | cut -d'=' -f2 | awk '{print $2}' > $TMP/${setname}_all.sri2
    printf "done\n"
    flag=1
    tmplmfeat="$tmplmfeat $TMP/${setname}_all.sri2"
  fi
fi

if [ $flag = 1 ]; then
  paste $TMP/${setname}_all.words $tmplmfeat | tr '\t' ' ' > $TMP/${setname}_all.lm
else
  printf "Error!!! No language model feature computed\n"
  return
fi

python $BINDIR/ExFt_bin/LM_feature.py $BASEDIR $setname $TMP/${setname}_all.lm





