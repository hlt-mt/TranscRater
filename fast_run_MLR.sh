#/bin/bash run the QE process on multiple microphones


export BINDIR=`pwd`
export BASEDIR=`pwd`
export RANKLIBDIR=/home/jalalvand/Desktop/toolkits/RankLib-v2.1/bin # in order to use MLR models you need to have RankLib library 

export CHANNELS=5  # Since there are 5 transcription channels in the data files


mkdir -p $BASEDIR/temp
mkdir -p $BASEDIR/temp/MLR


export MLR_Tune=No  # Set it to "Yes" if you want to optimize the parameters on Training set

# ./MLR_train.sh train_data  k-fold  models
. $BINDIR/MLR-QE/MLR_train.sh  MLR_train_LEX_LM_POS.data 5 MLR_models

# ./MLR_test.sh  test_data  models  output
. $BINDIR/MLR-QE/MLR_test.sh   MLR_test_LEX_LM_POS.data MLR_models MLR_output.prank



