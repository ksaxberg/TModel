#!/bin/bash
if [ $# == 0 ]
  then
	echo "Enter target folder containing files" 1>&2
	exit 1
fi

FOLDER=${1}
IDENTIFIER=${2}
#echo "Running files from: ${FOLDER}"
if [[ $# == 2 ]]
  then
        python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt
    if [ -f "img.png" ]
      then
         mv img.png ${IDENTIFIER}.gravity.png
         xdg-open ${IDENTIFIER}.gravity.png
    fi
else

    python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt
    xdg-open img.png
fi
