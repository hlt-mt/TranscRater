# Run RANKLIB Random Forest

trainFile=$1
folds=$2
modelsdir=$3


best_parameters="-ranker 8 -bag 50 -tree 20 -leaf 10";


# ----------------- Train/valid RR models
mkdir -p $modelsdir

if [[ $MLR_Tune = "Yes" ]]; then
  printf "MLR parameter tuning ..."
  for bg in 10 50 100 300; do
  for tr in 5 10 20; do
  for lf in 5 10 20; do
    printf "%sranker %d %sbag %d %stree %d %sleaf %d " - $type - $bg - $tr - $lf
    java -jar  $RANKLIBDIR/RankLib-2.6.jar -train $trainFile \
                                           -ranker $type -bag $bg -tree $tr -leaf $lf \
                                           -srate 0.1 -frate 0.5 -shrinkage 0.5 -tc 1 -mls 10  \
			                   -kcv $folds -norm zscore \
                                           -metric2t NDCG@${CHANNELS} -metric2T NDCG@${CHANNELS}  2>&1 | grep "Total" | awk '{print $NF}'                                                                       
  done
  done
  done > $BASEDIR/temp/MLR/train.log
  
  best_parameters=`cat $BASEDIR/temp/MLR/train.log | sort -n -k 9 -r | head -n 1 | cut -d' ' -f-8`  
fi


printf "\nTrain MLR models on \"$trainFile\" with best parameters of \"$best_parameters\" ..."
trainData=$trainFile #$BASEDIR/temp/folds/shuffled_train.data
java -jar  $RANKLIBDIR/RankLib-2.6.jar  -train $trainData  \
                                        $best_parameters \
                                        -srate 0.1 -frate 0.5 -shrinkage 0.5 -tc 1 -mls 10  \
					-norm zscore \
                                        -metric2t NDCG@${CHANNELS} -save  $modelsdir/MLR.model   2>&1 | grep WriteNothing

printf "done\n"                            

# --------------- Test on Train

. $BINDIR/MLR-QE/MLR_test.sh $trainFile $modelsdir $BASEDIR/temp/MLR/train.prank

