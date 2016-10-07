#Script to parse the input matrices.
import numpy as np

def parseDistance(filename):
	f = open(filename);
	x = f.readlines();
	matrix = np.zeros([len(x), len(x)]);
	#Assuming comma delimited, no lines but distance lines
	for i in range(len(x)):
		temp = x[i].split(',');
		for j in range(len(x)):
			current = temp[j];
			current = float(current.strip());
			matrix[i][j] = current;
	return matrix;

def parseDistanceUpperTriagular(filename):
	f = open(filename);
	x = f.readlines();
	matrix = np.zeros([len(x), len(x)]);
	#Assuming comma delimited, no lines but distance lines
	for i in range(len(x)):
		temp = x[i].split(',');
		for j in range(i,len(x)):
			current = temp[j-i];
			current = float(current.strip());
			matrix[i][j] = current;
	return matrix;

def parsePopulation(filename):
	f = open(filename);
	x = f.readlines();
	d = {};
	for i in range(len(x)):
		temp = x[i].split(',');
		d[i] = [float(temp[1].strip()), temp[0].strip()];
	return d
