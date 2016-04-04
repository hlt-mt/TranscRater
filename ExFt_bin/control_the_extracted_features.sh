# Control the Features Extracted

BASEDIR=$1
setname=$2
channel=$3

if [[ `cat $BASEDIR/data/${setname}/Features/${setname}_${channel}_A.Feat | wc | awk '{print $2/$1}'` = 12 ]]; 
then echo "ASR Features OK for LINK $channel..."; else "Error in ASR Features of LINK $channel..."; fi

if [[ `cat $BASEDIR/data/${setname}/Features/${setname}_${channel}_T.Feat | wc | awk '{print $2/$1}'` = 10 ]]; 
then echo "Textual Features OK for LINK $channel..."; else "Error in Textual Features of LINK $channel..."; fi

if [[ `cat $BASEDIR/data/${setname}/Features/${setname}_${channel}_W.Feat | wc | awk '{print $2/$1}'` = 23 ]]; 
then echo "Wordbased Features OK for LINK $channel..."; else "Error in Wordbased Features of LINK $channel..."; fi



