#!/bin/bash
if [ $# == 0 ]
  then
	echo "Enter target folder containing files" 1>&2
	exit 1
fi

FOLDER=${1}
echo "Running files from: ${FOLDER}"
python gravity.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt > out.gravity.${FOLDER}.txt
python gravitySum.py ${FOLDER}/population.txt ${FOLDER}/distanceEdge.txt ${FOLDER}/measuredDataEdge.txt > out.gravitySum.${FOLDER}.txt
if [ -f "Gravity.png" ]
  then
     mv Gravity.png ${FOLDER}.Gravity.png
     xdg-open ${FOLDER}.Gravity.png
fi
if [ -f "GravitySum.png" ]
  then
     mv GravitySum.png ${FOLDER}.GravitySum.png
     xdg-open ${FOLDER}.GravitySum.png
fi
