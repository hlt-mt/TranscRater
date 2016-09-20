
input=$1
ref=$2

cat $ref | cut -d' ' -f1 | while read id; do printf "$id ";cat $input | grep -i $id | awk '{print $5}' | tr '\n' ' '; echo ""; done 
