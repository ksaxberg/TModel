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
	analysis = np.zeros([20,6])
	for beta in np.arange(0.1, 2.1, .1):
		i = int(10*beta)
		gravityBeta = []
		roads = []
		mean = 0
		for j, k in indices:
			gravityBeta.append(gravitys[j][k] / (dist[j][k]**beta))
			mean += roadData[j][k]
			roads.append(roadData[j][k])
		mean /= len(indices)
		analysis[i-1][0] = beta;
		analysis[i-1][1] = regressionNoIntercept(gravityBeta, roads);
		predicted = [analysis[i-1][1]*x for x in gravityBeta]
		analysis[i-1][2] = rSquared(predicted, roads, mean);
		analysis[i-1][3], analysis[i-1][4] = regressionIntercept(gravityBeta, roads) 
		predicted = [analysis[i-1][3]*x+analysis[i-1][4] for x in gravityBeta]
		analysis[i-1][5] = rSquared(predicted, roads, mean)
	return analysis
		

def regressionNoIntercept(gravityBeta, roads):
	# Solving the linear regression y = mx
	#   where x = GravityEstimate
	#         y = RoadData
	#  This means running lstsq on x\y
	x_values = np.array(gravityBeta)
	y_values = np.array(roads)
	A = np.vstack([x_values]).T
	slope = np.linalg.lstsq(A,y_values)[0]
	return slope

def regressionIntercept(gravityBeta, roads):
	x_values = np.array(gravityBeta)
	y_values = np.array(roads)
	A = np.vstack([x_values, np.ones(len(x_values))]).T
	slope, intercept = np.linalg.lstsq(A,y_values)[0]
	return [slope, intercept]
	

def rSquared(predicted, actual, mean):
	# sum(predicted - actual)^2
	# divided by sum(predicted - mean)^2
	top = 0
	bottom = 0
	for i in range(len(predicted)):
		top += (predicted[i]-actual[i])**2
		bottom += (predicted[i] - mean)**2
	return 1-(top/bottom)
	

if __name__ == '__main__':
	import sys
	import parseData
	if((len(sys.argv)==4 and sys.argv[0]=="gravity.py" )):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		analysis = gravity(pop, dist, roadData);
		print("[Beta, Slope, R^2, slope, intercept, R^2]")
		print(analysis)
		#for i in range(20):
		#	print("i: ",i)
		#	pprint.pprint(roadData*analysis[i][1])
