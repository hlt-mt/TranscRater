#!/bin/bash Extract signal features

setname=$1

printf "    Extract Signal features for $setname..."

if [[ ! -e $OPENSMILEDIR ]]; then
  printf "ERROR!!! OpenSmile library not found in OPENSMILE=\"$OPENSMILE\"\n"
  return
fi


if [[ $setname = "train" ]]; then
  wavChannels=(${train_wavChannels[*]})
elif [[ $setname = "test" ]]; then
  wavChannels=(${test_wavChannels[*]})
else
  printf "Error!!! Define the set name train or test\n"
  return
fi


for mic in $(seq 1 $MICROPHONES)
do
  . $BINDIR/ExFt_bin/SIG_feature.sh ${wavChannels[$(($mic-1))]} $BASEDIR/data/features/${setname}_Mic_${mic}_SIG.feat &
done
wait


ch=0
for mic in $(seq 1 $MICROPHONES)
do
  for asr in $(seq 1 $ASR_SYSTEMS)
  do
    ch=$((ch+1))
    cp $BASEDIR/data/features/${setname}_Mic_${mic}_SIG.feat $BASEDIR/data/features/${setname}_CH_${ch}_SIG.feat
  done
done   

printf "done\n"
