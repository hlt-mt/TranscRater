#/bin/bash run ASR QE for CHiME3 data with multiple microphones

#set -e 

setname=$1

if [[ ! $setname = "train" ]] && [[ ! $setname = "test" ]]; then
  echo "Error!!! Define a set either \"train\" or \"test\""
  return
fi

echo "  Extract the features for $setname set..."

mkdir -p $BASEDIR/data/features



# ---------------- Extract WER scores for train set
if [[ $setname = "train" ]]; then
  if [ ! -e $trainREF ] || [[ $trainREF = "" ]]; then  # control the reference files
    echo "Error!!! The Reference for train set is not found"
    return
  fi

  tmpstr=""
  for ch in $(seq 1 $CHANNELS)
  do
    . $BINDIR/ExFt_bin/get_WER_scores.sh ${train_transcChannels[$((ch-1))]} $trainREF $BASEDIR/data/features/${setname}_CH_${ch}.wer
    tmpstr="$tmpstr $BASEDIR/data/features/${setname}_CH_${ch}.wer"
  done

  paste $tmpstr | tr '\t' ' ' | tr ' ' '\n' > $BASEDIR/temp/wer2rank_array
  python $BINDIR/bin/rank_array.py $BASEDIR/temp/wer2rank_array $CHANNELS $BASEDIR/data/features/${setname}.rankank

  for ch in $(seq 1 $CHANNELS)
  do
    cat $BASEDIR/data/features/${setname}.rank | cut -d' ' -f $ch >  $BASEDIR/data/features/${setname}_CH_${ch}.rank
  done
fi

# ---------------- Extract WER scores for test set
if [[ $setname = "test" ]]; then
  if [ ! -e $testREF ] || [[ $testREF = "" ]]; then  # control the reference files
    echo "Warning!!! The Reference for test set is not found"
    echo "           No evaluation on the test set will be provided"
  else
    tmpstr=""
    for ch in $(seq 1 $CHANNELS)
    do
      . $BINDIR/ExFt_bin/get_WER_scores.sh ${test_transcChannels[$((ch-1))]} $testREF $BASEDIR/data/features/${setname}_CH_${ch}.wer
      tmpstr="$tmpstr $BASEDIR/data/features/${setname}_CH_${ch}.wer"
    done
  
    paste $tmpstr | tr '\t' ' ' | tr ' ' '\n' > $BASEDIR/temp/wer2rank_array    
    python $BINDIR/bin/rank_array.py $BASEDIR/temp/wer2rank_array $CHANNELS  $BASEDIR/data/features/${setname}.rank
    
    for ch in $(seq 1 $CHANNELS)
    do
      cat $BASEDIR/data/features/${setname}.rank | cut -d' ' -f $ch >  $BASEDIR/data/features/${setname}_CH_${ch}.rank
    done
  fi
fi


# ---------------- Extract Signal Features (S)
if [[ $Feat == *SIG* ]]; then
    . $BINDIR/ExFt_bin/get_SIG_features.sh $setname
fi


# ---------------- Extract Lexical Features (P) 
if [[ $Feat == *LEX* ]]; then
  . $BINDIR/ExFt_bin/get_LEX_features.sh $setname
fi


# ---------------- Extract Language Model Features (LM)
if [[ $Feat == *LM* ]]; then
  . $BINDIR/ExFt_bin/get_LM_features.sh $setname
fi

 
# ---------------- Extract POS Features (P) 
if [[ $Feat == *POS* ]]; then
  . $BINDIR/ExFt_bin/get_POS_features.sh $setname
fi


# ---------------- Collect Features
if [[ $Feat == *_* ]]; then
  for ch in $(seq 1 $CHANNELS)
  do
    tmpfeat=""
    for feat in `echo $Feat|tr '_' ' '`
    do
      tmpfeat="$tmpfeat $BASEDIR/data/features/${setname}_CH_${ch}_${feat}.feat"
    done
    
    paste $tmpfeat | tr '\t' ' ' | sed "s/^ *//;s/ *$//;s/ \\{1,\\}/ /g" > $BASEDIR/data/features/${setname}_CH_${ch}_${Feat}.feat
  done
  #echo "Error!!! Not defined Feature type: \"$Feat\".... The defined types are \"S\" \"T\" \"W\" \"ST\" \"SW\" \"TW\" \"STW\" " 
fi
  

