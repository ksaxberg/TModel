#!/bin/bash
if [ $# == 0 ]
  then
	echo "Enter target folder containing files" 1>&2
	exit 1
fi

FOLDER=$1
echo "Running files from: $FOLDER"
python gravity.py $FOLDER/population.txt $FOLDER/distanceEdge.txt $FOLDER/measuredDataEdge.txt > out.gravity.txt
python gravitySum.py $FOLDER/population.txt $FOLDER/distanceEdge.txt $FOLDER/measuredDataEdge.txt > out.gravitySum.txt
xdg-open Gravity.png
xdg-open GravitySum.png
