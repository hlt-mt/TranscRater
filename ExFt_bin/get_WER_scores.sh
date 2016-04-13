#!/bin/sh    Extract WER scores

txtfile=$1
reffile=$2
outfile=$3

printf "    Extract WER scores..."
if [ ! -e $txtfile ] || [ ! -e $reffile ]
then
  echo "\nError!!! Either text file \"$txtfile\" or reference file \"$reffile\" is not available to compute the WER scores"
  return
fi


cat $txtfile | cut -d' ' -f 1 > $BASEDIR/temp/hypid
cat $reffile | cut -d' ' -f 1 > $BASEDIR/temp/refid

i=1
while read id;
do
  hypid=`sed -n "${i}p" $BASEDIR/temp/hypid`
  if [[ ! $id = $hypid ]]; then
    echo "\nError!!! hypothesis_id and reference_id miss-match in line ${i} $id VS. $hypid"
    return
  fi
  i=$(($i+1))
done < $BASEDIR/temp/refid

chmod 777 $BINDIR/bin/levenshtein
$BINDIR/bin/levenshtein $reffile $txtfile | head -n -1 | awk '{printf("%.3f\n",$NF/100)}' > $outfile

printf "done\n"
