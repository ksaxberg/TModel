#!/bin/bash
if [ $# == 0 ]
  then
	echo "Enter target folder containing files" 1>&2
	exit 1
fi

FOLDER=${1}
IDENTIFIER=${2}
PERCENTAGE=${3}
echo "Running files from: ${FOLDER}"

if [[ ${PERCENTAGE} == "0" ]]
  then

    python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt 

    #python gravitySum.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt > out.gravitySum.${IDENTIFIER}.txt
else

python addNoise.py ${FOLDER}/measuredDataEdge.txt ${PERCENTAGE} > ${FOLDER}/measuredDataEdgeNoise.txt

python gravityBoth.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdgeNoise.txt 

#python gravitySum.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdgeNoise.txt > out.gravitySum.${IDENTIFIER}.txt

fi


if [ -f "Gravity.png" ]
  then
     mv Gravity.png ${IDENTIFIER}.Gravity.png
     xdg-open ${IDENTIFIER}.Gravity.png
fi
if [ -f "GravitySum.png" ]
  then
     mv GravitySum.png ${IDENTIFIER}.GravitySum.png
     xdg-open ${IDENTIFIER}.GravitySum.png
fi
if [ -f "img.png" ] 
  then
     mv img.png ${IDENTIFIER}.gravity.png
     xdg-open ${IDENTIFIER}.gravity.png
fi
