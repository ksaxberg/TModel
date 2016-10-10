# Runs a basic gravity law analysis, given the population table and distance table
import numpy as np
import pprint
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
		gravitys[i][j] = pop[i][0]*pop[j][0];
	# Now run over beta values, divide by distance^beta
	#  Dumping values into a matrix with beta, K, R^2
	analysis = np.zeros([20,3])
	for beta in np.arange(0.1, 2.1, .1):
		i = int(10*beta)
		gravityBeta = np.copy(gravitys)
		mean = 0
		for j, k in indices:
			gravityBeta[j][k] = gravityBeta[j][k] / (dist[j][k]**beta)
			mean += roadData[j][k]
		mean /= len(indices)
		analysis[i-1][0] = beta;
		analysis[i-1][1] = singleRegression(gravityBeta, roadData, indices);
		analysis[i-1][2] = rSquared(analysis[i-1][1], roadData, gravityBeta, indices, mean);
	return analysis
		

def singleRegression(gravityBeta, roadData, indices):
	# Solving the linear regression y = mx
	#   where x = GravityEstimate
	#         y = RoadData
	#  This means running lstsq on x\y
	x_values = np.zeros([len(indices), 1])	
	y_values = np.zeros([len(indices), 1])

	index = 0
	for i,j in indices:
		x_values[index] = gravityBeta[i][j]
		y_values[index] = roadData[i][j]
		index += 1
	slope = np.linalg.lstsq(x_values,y_values)[0]
	return slope

def rSquared(k, roadData, gravityBeta, indices, mean):
	# for numpy arrays, array*array should define element by element multiplication
	top = 0
	bottom = 0
	for i,j in indices:
		top += (k*gravityBeta[i][j]-roadData[i][j])**2
		bottom += (roadData[i][j] - mean)**2
	return 1-(top/bottom)
	

if __name__ == '__main__':
	import sys
	import parseData
	if((len(sys.argv)==4 and sys.argv[0]=="gravity.py" )):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		analysis = gravity(pop, dist, roadData);
		print("[Beta, Slope, R^2]")
		print(analysis)
		#for i in range(20):
		#	print("i: ",i)
		#	pprint.pprint(roadData*analysis[i][1])
