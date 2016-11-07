#Script to parse the input matrices.
import numpy as np

def parseDistance(filename):
	f = open(filename)
	x = f.readlines()
	matrix = np.zeros([len(x), len(x)])
	#Assuming comma delimited, no lines but distance lines
	for i in range(len(x)):
		temp = x[i].split(',')
		for j in range(len(x)):
			current = temp[j]
			current = float(current.strip())
			matrix[i][j] = current
	f.close()
	return matrix

def parseEdges(filename, keys):
	f = open(filename)
	matrix = np.zeros([len(keys), len(keys)])
	#Assuming each line is unique			
	for line in f:
		place1, place2, value = line.strip().split(',')
		ind1 = keys[place1.strip()]
		ind2 = keys[place2.strip()]
		#Make ind1 the smaller, upper triang matrix
		if ind1 > ind2:
			ind1, ind2 = ind2, ind1
		#Assuming uniqueness, multiple listings is added when desired 
		matrix[ind1][ind2] += float(value.strip())
	f.close()
	return matrix	

def makeKeys(filename):
	#Assuming working with the population file
	f = open(filename)
	d = {}
	for i, line in enumerate(f):
		key = line.strip().split(',')[0].strip()	
		d[key] = i
	return d

def parseDistanceUpperTriagular(filename):
	f = open(filename)
	x = f.readlines()
	matrix = np.zeros([len(x), len(x)])
	#Assuming comma delimited, no lines but distance lines
	for i in range(len(x)):
		temp = x[i].split(',')
		for j in range(i,len(x)):
			current = temp[j-i]
			current = float(current.strip())
			matrix[i][j] = current
	return matrix

def parsePopulation(filename):
	f = open(filename)
	x = f.readlines()
	d = {}
	for i in range(len(x)):
		temp = x[i].split(',')
		d[i] = [float(temp[1].strip()), temp[0].strip()]
	f.close()
	return d

