#/bin/bash run the QE process on multiple microphones


export BINDIR=`pwd`
export BASEDIR=`pwd`


export CHANNELS=5  # Since there are 5 transcription channels in the data files


mkdir -p $BASEDIR/temp
mkdir -p $BASEDIR/temp/RR


export RR_Iter=10  # set the number of training iterations

# ./RR_train.sh train_data  k-fold  models
. $BINDIR/REG-QE/RR_train.sh  RR_train_LEX_LM_POS.data 5 RR_models
  
# ./RR_test.sh  test_data  models  output
. $BINDIR/REG-QE/RR_test.sh   RR_test_LEX_LM_POS.data RR_models RR_output.pwer


