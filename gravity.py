# Runs a basic gravity law analysis, given the population table and distance table
import numpy as np
from scipy import stats
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
	travel = []
	for i,j in indices:
		gravitys[i][j] = pop[i][0]*pop[j][0];
		travel.append(roadData[i][j])
	# Now run over beta values, divide by distance^beta
	#  Dumping values into a matrix with beta, K, R^2
	analysis = np.zeros([20,6])
	for beta in np.arange(0.1, 2.1, .1):
		i = int(10*beta)
		gravityBeta = []
		for j, k in indices:
			gravityBeta.append(gravitys[j][k] / (dist[j][k]**beta))
		analysis[i-1][0] = beta;
		analysis[i-1][1] = regressionNoIntercept(gravityBeta, travel)
		predicted = [analysis[i-1][1]*x for x in gravityBeta]
		analysis[i-1][2] = rSquared(predicted, travel)
		#print("Predicted: ")
		#pprint.pprint(predicted)
		#print("Actual: ")
		#pprint.pprint(travel)
		analysis[i-1][3], analysis[i-1][4] = regressionIntercept(gravityBeta, travel) 
		predicted = [(analysis[i-1][3]*x+analysis[i-1][4]) for x in gravityBeta]
		analysis[i-1][5] = rSquared(predicted, travel)
	return analysis
		

def regressionNoIntercept(gravityBeta, travel):
	# Solving the linear regression y = mx
	#   where x = GravityEstimate
	#         y = RoadData
	#  This means running lstsq on x\y
	x_values = np.array(gravityBeta)
	y_values = np.array(travel)
	A = np.vstack([x_values]).T
	slope = np.linalg.lstsq(A,y_values)[0]
	return slope

def regressionIntercept(gravityBeta, travel):
	x_values = np.array(gravityBeta)
	y_values = np.array(travel)
	A = np.vstack([x_values, np.ones(len(x_values))]).T
	slope, intercept = np.linalg.lstsq(A,y_values)[0]
	#slope2, intercept2, r_value, p_value, std_err = stats.linregress(gravityBeta, travel)
	#print("Slope: ", slope2)
	#print("Intercept: ", intercept2)
	#print("R^2: ", r_value**2)
	return [slope, intercept]

def rSquared(predicted, actual):
	# sum(predicted - actual)^2
	# divided by sum(predicted - mean)^2
	#SSE = sum([(actual[i] - predicted[i])**2 for i in range(len(predicted))])
	mean = sum(actual)/len(actual)
	SSTO = sum([(actual[i] - mean)**2 for i in range(len(predicted))])
	SSR = sum([(predicted[i]-mean)**2 for i in range(len(predicted))])
	#return 1-(SSE/SSTO)
	return SSR/SSTO
	
	

if __name__ == '__main__':
	import sys
	import parseData
	if(len(sys.argv)==4  ):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		analysis = gravity(pop, dist, roadData);
		print("[Beta, Slope, R^2, slope, intercept, R^2]")
		print(analysis)
