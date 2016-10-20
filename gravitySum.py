import sys
import gravity
import math

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
		if i != source and (source,i) not in memory and (i,source) not in memory:
			# Add this to memory then
			if i < source:
				memory[(i, source)] = [S[i], PathSoFar[i]]
			else:
				memory[(source, i)] = [S[i], PathSoFar[i]]
	return S[destination]	
		
def overLappingRoutes(distances):
	#Have spoiler route index -1
	#Just trying to make a collection of empty lists
	listOfLists = []
	for i in range(len(distances[0])):
		listOfLists.append([])
	routeOverlap = list(listOfLists)
	for i in range(len(distances[0])):
		routeOverlap[i] = list(listOfLists)
	# Finished collection of empty lists
	memory = {}
	for i in range(len(distances[0])):
		for j in range(len(distances[0])):
			#TODO: Don't leave this n^2
			#Who doesn't like an n^2 pass
			# Sparse Matrix - run on edges, not vertex*vertex
			runDijkstra(distances, i, j, memory)
	for key,value in memory.items():
		# For each consecutive pair in the path
		for i in range(len(value[1])-1):
			r1 = value[1][i]
			r2 = value[1][i+1]
			# Store the fact that the parent route goes over edge, 
			#  and total distance of the path. 
			#TODO: Fix this representation, storing same data multiple times
			val = value[0]
			routeOverlap[r1][r2].append((key, value[0]))
			routeOverlap[r2][r1].append((key, value[0]))
	return routeOverlap	

def gravitySum(pop, distances, roadData):
	#Making the distance matrix symmetric
	for i in range(len(distances)):
		for j in range(len(distances)):
			if distances[i][j] == 0 and distances[j][i] != 0:
				distances[i][j] = distances[j][i]
			if distances[j][i] == 0 and distances[i][j] != 0:
				distances[j][i] = distances[i][j]
	overlap = overLappingRoutes(distances)
	#Need to format into 3 lists, RoadData, Gravity, Distance
	# All indexed in order
	print(overlap)	
	


if __name__ == '__main__':
	import sys
	import parseData
	if(len(sys.argv)==4  ):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		x,y,z = formatRawMatrices(pop, dist, roadData);
		analysis = runGravity(x,y,z);
		print("[Beta, Slope, R^2, slope, intercept, R^2]")
		pprint.pprint(analysis)
