#!/bin/bash Extract Signal features for each channel

wavlist=$1
outfile=$2

while read wavfile
do
  $OPENSMILEDIR/SMILExtract -C $BINDIR/conf/MFCC12_E_D_A_Z.conf -I $wavfile -O ${wavfile}.mfcc.csv 2>&1 | grep writeNothing
  $OPENSMILEDIR/SMILExtract -C $BINDIR/conf/prosodyShs.conf -I $wavfile -O ${wavfile}.pro.csv 2>&1 | grep writeNothing

  cat ${wavfile}.mfcc.csv| sed -n '1,$p' | tr ';' ' ' \
                                          | awk '{n++;for(i=2;i<=NF;i++) sum[i]=$i}END{for(i=2;i<=NF;i++) printf("%.4f ",sum[i]);printf("\n")}' > ${wavfile}.mfcc.feat
  cat ${wavfile}.pro.csv | sed -n '1,$p' | tr ';' ' ' \
                                          | awk '{n++;for(i=2;i<=NF;i++) sum[i]=$i}END{for(i=2;i<=NF;i++) printf("%.4f ",sum[i]);printf("\n")}' > ${wavfile}.pro.feat

  paste ${wavfile}.mfcc.feat ${wavfile}.pro.feat | tr '\t' ' ' | sed "s/^ *//;s/ *$//;s/ \\{1,\\}/ /g"
  rm ${wavfile}.*
done < $wavlist > ${outfile}

