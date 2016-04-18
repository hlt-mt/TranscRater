# Rank the Systems

inputfile=$1

cat $inputfile | awk '{ if( index($L,"=") >0 && index($L,"#") != 1 ) print "export",$L; else print $L }' > ${inputfile}.exp

. ${inputfile}.exp

export CHANNELS=$(($MICROPHONES*$ASR_SYSTEMS))


feature_set=(SIG LEX LM POS)
unset ffeat

i=0
for feat in $F_SIG $F_LEX $F_LM $F_POS; do
  if [ $feat = 1 ]; then
    ffeat="${ffeat}_${feature_set[$i]}"
  fi
  i=$(($i+1))
done
export Feat=${ffeat/_/}

if [[ $Feat = "" ]]; then
  printf "Error!!! No Feature is defined...\n"
  return
fi

rm ${inputfile}.exp


# User's configuration problem

# Transciprion files
for transc in `echo ${train_transcChannels[*]}`; do
  if [ ! -e $transc ]; then
    printf "ERROR!!! Transcription file $transc does not exist...\n"
    return
  fi
done
for transc in `echo ${test_transcChannels[*]}`; do
  if [ ! -e $transc ]; then
    printf "ERROR!!! Transcription file $transc does not exist...\n"
    return
  fi
done


# Feature Selection

# Lexicon Features
if [ $F_LEX = 1 ]; then
  if [ ! -e $LEXFEAT ]; then
    printf "ERROR!!! You asked for Lexicon based features but $LEXFEAT does not exist...\n"
    return
  fi
fi

# Language model features
if [ $F_LM = 1 ]; then
  if [ ! -e $RNNLMDIR/rnnlm ]; then
    printf "ERROR!!! You asked for LM features but $RNNLMDIR/rnnlm does not exist...\n"
    return
  fi
  if [ ! -e $SRILMDIR/ngram ]; then
    printf "ERROR!!! You asked for LM features but $SRILMDIR does not exist...\n"
    return
  fi
fi

# Part-of-speech features
if [ $F_POS = 1 ]; then
  if [ ! -e $TREETAGDIR/tree-tagger ]; then
    printf "ERROR!!! You asked for POS based features but $TREETAGDIR/tree-tagger does not exist...\n"
    return
  fi
fi

# Signal based features
if [ $F_SIG = 1 ]; then
  if [ ! -e $OPENSMILEDIR/SMILExtract ]; then
    printf "Error!!! You asked for Signal features but OpenSmile tool is not ready in $OPENSMILEDIR/SMILExtract...\n"
    return
  fi
  for sig_list in `echo ${train_wavChannels[*]}`; do
    if [ ! -e $sig_list ]; then
      printf "Error!!! You asked for Signal features but $sig_list does not exist...\n"
      return;
    fi
  done
  for sig_list in `echo ${test_wavChannels[*]}`; do
    if [ ! -e $sig_list ]; then
      printf "Error!!! You asked for Signal features but $sig_list does not exist...\n"
      return;
    fi
  done
fi


# Machine Learninig


      
