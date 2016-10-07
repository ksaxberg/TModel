#Runs a basic gravity law analysis, given the population table and distance table
import numpy as np

def gravity(pop, dist, roadData):
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
	analysis = np.zeros(20,3);
	for beta in np.arange(0.1, 2.0, .1):
		i = int(10*beta);
		analysis[i][0] = beta;
		analysis[i][1] = singleRegression(gravitys, beta, pop, dist);
		analysis[i][2] = rSquared(analysis[i][1], beta, pop, dist, roadData);
		

def singleRegression(gravitys, beta, pop, dist):
	
def rSquared(k, beta, pop, dist, roadData):
	

if __name__ == '__main__':
	import sys
	import parseData
	if((len(sys.argv)==4 and sys.argv[0]=="gravity.py" )):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3];
		gravity(pop, dist, roadData);
