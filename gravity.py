#Runs a basic gravity law analysis, given the population table and distance table
import numpy as np

def gravity(pop, dist):
	gravitys = np.zeros(dist.shape);
	dim = len(pop.keys());
	# Find non-zero indices first, create shortlist
	indices = [];
	for i in range(dim):
		for j in range(i, dim):
			if(dist[i][j] != 0):
				indices.append((i,j));
	# Start with population product in gravity matrix
	for i,j in indices:
		if(dist[i][j] != 0):
			gravitys = pop[i][0]*pop[j][0];
	# Now run over beta values, divide by distance^beta
	#  Dumping values into a matrix with beta, K, R^2
	

	print("Got to the function alright");


if __name__ == '__main__':
	import sys
	import parseData
	if((len(sys.argv)==3 and sys.argv[0]=="gravity.py" )):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		gravity(pop, dist);
