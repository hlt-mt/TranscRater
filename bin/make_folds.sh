# make K-fold cross validation on TRAINING set

trainFile=$1
folds=$2


mkdir -p $BASEDIR/temp/folds

printf "Make %d fold data..." $folds


N=`cat $trainFile | cut -d' ' -f2 | sort | uniq | wc -l`
part=`echo $N/$folds | bc | awk '{print $1+1}'`

shuf_all=(`cat $trainFile | cut -d' ' -f2 | sed 's/qid://g' | sort | uniq | shuf`)

for fld in $(seq 1 $folds)
do 

  sbeg=`echo $fld|awk -v "p=$part" '{print ($1-1)*p}'`;   
  shuf_tst=(`echo ${shuf_all[*]:$sbeg:$part}`);
  shuf_trn=(`echo ${shuf_all[*]} ${shuf_tst[*]} | tr ' ' '\n' | sort | uniq -c | awk '{if($1==1) printf("%s ",$2)}'`)
  
  for qid in `echo ${shuf_trn[*]}`
  do
    grep " qid:$qid " $trainFile
  done > $BASEDIR/temp/folds/fold_${fld}_train.data

  for qid in `echo ${shuf_tst[*]}`
  do
    grep " qid:$qid " $trainFile
  done > $BASEDIR/temp/folds/fold_${fld}_test.data

done

for qid in `echo ${shuf_all[*]}`
do
  grep " qid:$qid " $trainFile
done > $BASEDIR/temp/folds/shuffled_train.data

printf "done\n"
