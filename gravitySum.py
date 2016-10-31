import sys
import pprint
import numpy as np
from gravity import *
import math
DEBUG = True

def formatMatrixAsList(someMatrix):
	# Assumption that matrix is square
	listy = []
	size = len(someMatrix[0])	
	for i in range(size):
		for j in range(i,size):
			if (someMatrix[i][j] != 0):
				listy.append(someMatrix[i][j])
	return listy

def runDijkstra(distances, source, destination, memory ):
	# Distances is a formatted, symmetric matrix (assuming undirected graph)
	#  0 indicates no edge presences
	#  Naive implementation of Dijkstras, not for efficiency
	#  distances[0] should retrieve row 0, indicating distance from 0 to every other point
	#  symmetric matrix allows for starting with distance[i]
	if (source, destination) in memory:
		return memory[(source, destination)]
	if (destination, source) in memory:
		return memory[(destination, source)]
		
	# S is colleciton of shortest decided distances already
	S = {source: 0}
	PathSoFar = {source: [source]}
	D = {i:distances[source][i] for i in range(len(distances[0])) if distances[source][i] != 0}	
	for key,value in D.items():
		PathSoFar[key] = [source, key]
	while destination not in S.keys():
		minim = min(D.values())
		newMin = [key for key, value in D.items() if value == minim]
		newMin = newMin[0]
		#Dealing with newMin item. (node, distance)
		S[newMin] = minim
		del D[newMin]
		distFromNew = distances[newMin]
		for key,value in D.items():
			# Replace all distances that need replacing
			if distFromNew[key] != 0 and value > minim + distFromNew[key]:
				newValue = minim + distFromNew[key]
				D[key] = newValue
				#Replace path with newly found shorter one
				PathSoFar[key] = list(PathSoFar[newMin])
				PathSoFar[key].append(key)
		for x in range(len(distances[0])):
			if x in S.keys() or distFromNew[x]==0:
				continue
			#For nonfinished indices 
			elif x not in D.keys() :
				D[x] = distFromNew[x]+minim
				# Add paths for newly found elements
				PathSoFar[x] = list(PathSoFar[newMin])
				PathSoFar[x].append(x)
	#Only adding completed routes to the memory, things in S
	for i in S.keys():
		if (i != source) and ((source,i) not in memory) and ((i,source) not in memory):
			# Add this to memory then
			if i < source:
				memory[(i, source)] = [S[i], PathSoFar[i]]
			else:
				memory[(source, i)] = [S[i], PathSoFar[i]]
	return S[destination]	
		
def overLappingRoutes(distances):
	#Have spoiler route index -1
	#Just trying to make a collection of empty lists
	size = len(distances[0])
	routeOverlap = [[[] for i in range(size)] for j in range(size)]
	# Finished collection of empty lists
	memory = {}
	for i in range(size):
		for j in range(i,size):
			# Runs the Dijkstra calculation on the upper trianglular part
			# Sparse Matrix - run on edges, not vertex*vertex
			# Calculates how to get from A,B for every pair.
	 		runDijkstra(distances, i, j, memory)
	for key,value in memory.items():
		# For each consecutive pair in the path
		for i in range(len(value[1])-1):
			if value[1][i] < value[1][i+1]:
				r1 = value[1][i]
				r2 = value[1][i+1]
			else:
				r2 = value[1][i]
				r1 = value[1][i+1]
			# Store the fact that the parent route goes over edge, 
			#  and total distance of the path. 
			routeOverlap[r1][r2].append((key, value[0]))
	return routeOverlap	

def convertRoutesToList(overlaps, pops, beta, alpha):
	#Constant factor K will have to be multiplied on the size
	partialGravities = np.zeros([len(overlaps), len(overlaps)])
	for i, row in enumerate(overlaps):
		for j, col in enumerate(row):
			if col == []:
				continue
			for x in col:
				#For each x, add the partial gravity
				val = (pops[x[0][0]][0])*(pops[x[0][1]][0])
				val = val**alpha
				distance = x[1]**beta
				partialGravities[i][j]+=val/distance
	return partialGravities

def gravitySum(pop, distances, roadData):
	#Making the distance matrix symmetric
	for i in range(len(distances)):
		for j in range(len(distances)):
			if (distances[i][j] == 0) and (distances[j][i] != 0):
				distances[i][j] = distances[j][i]
			if (distances[j][i] == 0) and (distances[i][j] != 0):
				distances[j][i] = distances[i][j]
	overlap = overLappingRoutes(distances)
	#Need to format into 3 lists, RoadData, Gravity, Distance
	# All indexed in order
	for i in range(20):
		beta = i/10.0
		alpha = 1
		partialGravities = convertRoutesToList(overlap, pop, beta, alpha)
		partialList = formatMatrixAsList(partialGravities)
		roadDataList = formatMatrixAsList(roadData)
		slope, intercept = regressionIntercept(partialList, roadDataList)
		#TODO: This does not verify the calibration, need different prediction
		#  as have calibrated on the overlapping routes
		#TODO: R^2 here does nothing to verify the predictive quality
		predicted = [slope*x+intercept for x in partialList]
		r2 = rSquared(predicted, roadDataList)	
		print("Beta: {}\tAlpha: {}\nSlope: {}\tIntercept: {}\tR^2: {}".format(
			beta, alpha, slope, intercept, r2))


if __name__ == '__main__':
	import sys
	import parseData
	if(len(sys.argv)==4  ):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		x,y,z = formatRawMatrices(pop, dist, roadData);
		gravitySum(pop, dist, roadData)
		#analysis = runGravity(x,y,z);
		#print("[Beta, Slope, R^2, slope, intercept, R^2]")
		#pprint.pprint(analysis)
