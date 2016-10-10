# Runs a basic gravity law analysis, given the population table and distance table
import numpy as np
from sklearn import linear_model

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
		gravitys = pop[i][0]*pop[j][0];
	# Now run over beta values, divide by distance^beta
	#  Dumping values into a matrix with beta, K, R^2
	analysis = np.zeros(20,3)
	for beta in np.arange(0.1, 2.0, .1):
		i = int(10*beta)
		gravityBeta = gravitys
		mean = 0
		for i, j in indices:
			gravityBeta[i][j] = gravityBeta[i][j] / (distance[i][j]**beta)
			mean += gravityBeta[i][j]
		mean /= len(indices)
		analysis[i][0] = beta;
		analysis[i][1] = singleRegression(gravityBeta, roadData, indices);
		analysis[i][2] = rSquared(analysis[i][1], gravityBeta, roadData, indices, mean);
	return analysis
		

def singleRegression(gravityBeta, roadData, indices):
	# from scipy import stats
	x_values = []
	y_values = []
	for i,j in indices:
		x_values.append(gravityBeta[i][j])
		y_values.append(roadData[i][j])
	#slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
	#print("Slope: %f\nIntercept: %f\nr_value: %f" % [slope, intercept, r_value])
	model = linear_model.LinearRegression(fit_intercept = False)
	fit = model.fit(x_values, y_values)
	return fit.intercept
	
def rSquared(k, gravityBeta, roadData, indices, mean):
	# for numpy arrays, array*array should define element by element multiplication
	top = 0
	bottom = 0
	for i,j in indices:
		top += (gravityBeta[i][j] - k*roadData[i][j])**2
		bottom += (gravityBeta[i][j] - mean)**2
	return 1-(top/bottom)
	

if __name__ == '__main__':
	import sys
	import parseData
	if((len(sys.argv)==4 and sys.argv[0]=="gravity.py" )):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		analysis = gravity(pop, dist, roadData);
		print(analysis)
