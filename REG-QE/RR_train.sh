#!/bin/bash Train Ranking by Regression Models (RR)

trainFile=$1
folds=$2
modelsdir=$3


printf "\nTrain RR Models on \"$trainFile\" ...\n"

mkdir -p $BASEDIR/temp/RR


trainLabel=$BASEDIR/temp/RR/train.label
trainFeat=$BASEDIR/temp/RR/train.feat
testLabel=$BASEDIR/temp/RR/test_label
testFeat=$BASEDIR/temp/RR/test_feat
results=$BASEDIR/temp/RR/results
  
cat $trainFile | cut -d' ' -f1 > $trainLabel
cat $trainFile | tr ':' ' ' | awk '{for(i=5;i<=NF;i+=2) printf("%.4f ",$i); printf("\n")}' > $trainFeat
  
mkdir -p $testLabel
mkdir -p $testFeat
mkdir -p $results
mkdir -p $modelsdir

cp $trainLabel $testLabel/test.label
cp $trainFeat  $testFeat/test.feat
  
# --------------- train Extremely Randomized Tree

if [[ $RR_Iter ]]; then
  python $BINDIR/bin/my_batch_et.py --scale -i $RR_Iter  --select_features -d' ' --folds $folds --output_folder $results \
                                  $trainFeat $trainLabel $modelsdir $testFeat $testLabel 2>&1 | grep WriteNothing
else
  python $BINDIR/bin/my_batch_et.py --scale -i 30  --select_features -d' ' --folds $folds --output_folder $results \
                                  $trainFeat $trainLabel $modelsdir $testFeat $testLabel 2>&1 | grep WriteNothing
fi                                                                       

# --------------- Test on Train

. $BINDIR/REG-QE/RR_test.sh $trainFile $modelsdir $BASEDIR/temp/RR/train.pwer

