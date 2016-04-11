#/bin/bash run the QE process on multiple microphones


# cd to the directory of CHiME3 example and run the following commands



# 1)
# set the inputs and paths for the framework, libraries and the models

configfile=$1

if [[ $configfile = "" ]] || [[ ! -e $configfile ]]; then
  echo "Error!!! Configuration file not found..."
  return
fi

. $configfile
. $BINDIR/bin/run_config.sh $configfile


mkdir -p $BASEDIR/temp
mkdir -p $BASEDIR/data
mkdir -p $BASEDIR/results
mkdir -p $BASEDIR/temp/RR
mkdir -p $BASEDIR/temp/MLR


# 2) 
# Get the features for training set
. $BINDIR/bin/get_the_features.sh train


# 3) 
# Get the features for training set
. $BINDIR/bin/get_the_features.sh test


# 4) 
# Run QE 
if [[ $QE = *RR* ]]; then
  # Prepare data for RR approach
  . $BINDIR/REG-QE/RR_data.sh train

  # train RR models
  . $BINDIR/REG-QE/RR_train.sh  $BASEDIR/data/RR_train_${Feat}.data $folds $BASEDIR/models/RR_models
  
  # Prepare data for RR approach
  . $BINDIR/REG-QE/RR_data.sh test

  # test RR models
  . $BINDIR/REG-QE/RR_test.sh  $BASEDIR/data/RR_test_${Feat}.data $BASEDIR/models/RR_models $BASEDIR/results/RR_${Feat}.pwer
fi


# 5)

if [[ $QE = *MLR* ]] && [[ `echo $CHANNELS'>'1|bc -l` = 1 ]]; then
  # Prepare data for RR approach
  . $BINDIR/MLR-QE/MLR_data.sh train

  # train RR models
  . $BINDIR/MLR-QE/MLR_train.sh  $BASEDIR/data/MLR_train_${Feat}.data $folds $BASEDIR/models/MLR_models

  # Prepare data for RR approach
  . $BINDIR/MLR-QE/MLR_data.sh test

  # test RR models
  . $BINDIR/MLR-QE/MLR_test.sh  $BASEDIR/data/MLR_test_${Feat}.data $BASEDIR/models/MLR_models $BASEDIR/results/MLR_${Feat}.prank
fi


