#!/bin/bash
if [ $# == 0 ]
  then
	echo "Enter target folder containing files" 1>&2
	exit 1
fi

FOLDER=${1}
IDENTIFIER=${2}
PERCENTAGE=${3}
#echo "Running files from: ${FOLDER}"
if [[ $# == 3 ]] 
  then 
    if [[ ${PERCENTAGE} == "0" ]]
      then
    
        python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt 
    
    else
    
    python addNoise.py ${FOLDER}/measuredDataEdge.txt ${PERCENTAGE} > ${FOLDER}/measuredDataEdgeNoise.txt
    
    python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdgeNoise.txt 
    
    fi
else

    python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt 
fi

if [ -f "img.png" ] 
  then
     mv img.png ${IDENTIFIER}.gravity.png
     xdg-open ${IDENTIFIER}.gravity.png
fi
