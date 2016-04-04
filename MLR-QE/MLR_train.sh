# Run RANKLIB Random Forest

trainFile=$1
folds=$2
modelsdir=$3

type=8;
bg=100;
tr=15;
lf=15 # Optimum Values
# -srate 0.5 -shrinkage 0.8 -tc 256 -mls 5 \

# ----------------- Create fold lists
/bin/bash $BINDIR/bin/make_folds.sh $trainFile $folds


# ----------------- Train/valid RR models
mkdir -p $modelsdir

if [[ $TuneMLR = Yes ]]; then
  printf "MLR parameter tuning ..."
  for bg in 50 100 150; do
  for tr in 5 10 20; do
  for lf in 10 15 20; do
    printf "%sranker %d %sbag %d %stree %d %sleaf %d " - $type - $bg - $tr - $lf
    for fld in $(seq 1 $folds);  do
      java -jar  $RANKLIBDIR/RankLib_old.jar -train $BASEDIR/temp/folds/fold_${fld}_train.data -validate $BASEDIR/temp/folds/fold_${fld}_test.data \
                                             -ranker $type -bag $bg -tree $tr -leaf $lf \
                                             -srate 0.5 -shrinkage 0.8 -tc 256 -mls 5 \
                                             -norm zscore -metric2t NDCG@${CHANNELS} -metric2T NDCG@${CHANNELS}  2>&1 | grep "NDCG@${CHANNELS} on validation data:" | awk '{print $NF}'
                                                                             
    done | awk '{n++; sum+=$1} END {print sum/n}'
  done
  done
  done > $BASEDIR/temp/MLR/train.log
  
  best_parameters=`cat $BASEDIR/temp/MLR/train.log | sort -n -k 9 -r | head -n 1 | cut -d' ' -f-8`
  
  printf "\nTrain MLR models on \"$trainFile\"..."
  trainData=$BASEDIR/temp/folds/shuffled_train.data
  java -jar  $RANKLIBDIR/RankLib_old.jar  -train $trainData  ${best_parameters} \
                                          -srate 0.5 -shrinkage 0.8 -tc 256 -mls 5 -norm zscore -metric2t MAP \
                                          -save  $modelsdir/MLR.model   2>&1 | grep WriteNothing
  printf "done\n"

else
  printf "\nTrain MLR models on \"$trainFile\"..."
  trainData=$BASEDIR/temp/folds/shuffled_train.data
  java -jar  $RANKLIBDIR/RankLib_old.jar  -train $trainData  \
                                          -ranker $type -bag $bg -tree $tr -leaf $lf \
                                          -srate 0.5 -shrinkage 0.8 -tc 256 -mls 5 -norm zscore -metric2t MAP \
                                          -save  $modelsdir/MLR.model   2>&1 | grep WriteNothing

  printf "done\n"
fi                                          

# --------------- Test on Train

. $BINDIR/MLR-QE/MLR_test.sh $trainFile $modelsdir $BASEDIR/temp/MLR/train.prank
                                          
