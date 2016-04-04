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
  echo "Error!!! No Feature is defined"
  return
fi

#rm ${inputfile}.exp
