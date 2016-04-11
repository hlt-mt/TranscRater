#!/bin/bash Extract Part-Of-Speech features


setname=$1

printf "    Extract POS features for $setname..."

if [[ ! -e $TREETAGDIR ]]; then
  echo "Error!!! TreeTagger library not found in \"$TREETAGDIR\""
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
  echo "transcrater_start_of_channel_${ch}"
  cat  ${transcChannels[$((ch-1))]} | cut -d' ' -f2- | sed 's/<unk>/kioonia/g' | sed 's/$/ #/g' | tr ' ' '\n'             
done > $BASEDIR/temp/${setname}_all_POS.txt 

cat $BASEDIR/temp/${setname}_all_POS.txt | $TREETAGDIR/tree-tagger $BINDIR/AUXILIARY/english.par -quiet -token -lemma -sgml -prob -threshold 0.001 \
                                         | awk '{print $1,$2,$4}' > $BASEDIR/temp/${setname}_all_POS

python $BINDIR/ExFt_bin/POS_feature.py $BASEDIR $setname $BASEDIR/temp/${setname}_all_POS

#$SRILMDIR/ngram -lm $SRILMPOS -order 4 -ppl $TMP/${tmp}.hyp.upp.pos -debug 2 2>&1 \
#                            | grep " logprob= " | head -n -1 | awk '{print $4,log($NF)}' > $TMP/${tmp}.hyp.MF2

printf "done\n"
