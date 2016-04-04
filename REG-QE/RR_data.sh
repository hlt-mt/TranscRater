#/bin/bash RR data preparation for training the regressors

setname=$1


# ---------------- Utterance IDs

if [[ $setname = "train" ]]; then
  setlist=(`cat ${train_transcChannels[0]} | cut -d' ' -f 1`)
elif [[ $setname = "test" ]]; then
  setlist=(`cat ${test_transcChannels[0]} | cut -d' ' -f 1`)
else
  printf "\nERROR!!! Define a set name \"train\" or \"test\" for ./REG-QE/RR_data.sh"
  return
fi


# ---------------- Data Preparation

for segN in  $(seq 1 ${#setlist[*]})
do

  qid=${setlist[$(($segN-1))]}

  for ch in $(seq 1 $CHANNELS)
  do
    paste  $BASEDIR/data/features/${setname}_CH_${ch}.wer $BASEDIR/data/features/${setname}_CH_${ch}_${Feat}.feat | sed -n "${segN}p" \
           | awk -v "qid=$qid" '{printf("%.3f qid:%s",$1,qid) ; for(i=2;i<=NF;i++) printf(" %d:%.5f",i-1,$i); printf("\n")}';
  done

done > $BASEDIR/data/RR_${setname}_${Feat}.data

