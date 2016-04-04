
bbdir=/hltsrv2/jalalvand/Word-based_Feature_Extraction_Package
ppp="$bbdir/TreeTagger"
input=$1
cat $input | while read l; 
do 
  echo $l | tr ' ' '\n' | $ppp/bin/tree-tagger $ppp/lib/english.par -cap-heuristics | tr '\n' ' '; echo ""
done > ${input}.pos
