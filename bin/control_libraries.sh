

if [[ `python -c "import sklearn; print sklearn.__version__" 2>&1 | grep -i error` ]]; then
  printf "ERROR!!! \"sklearn\" library is not installed.\n"
fi


java_version=`java -version 2>&1 | head -n 1 | tr '"' ' '| awk '{printf($NF)}' | awk '{printf("%.1f\n",$1)}'`
if [[ `echo $java_version'<'1.8|bc -l` = 1 ]]; then
  printf "ERROR!!! java version $java_version is lower than 1.8. Machine learned ranking might not work properly.\n"
fi

if [ ! -e $RANKLIBDIR/RankLib-2.6.jar ]; then
  printf "ERROR!!! RankLib-2.6.jar does not exist in \"$RANKLIBDIR\". Machine learned ranking might not work.\n"
fi




