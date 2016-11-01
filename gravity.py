# Runs a basic gravity law analysis, given the population table and distance table
import numpy as np
import pprint

def formatRawMatrices(pop, dist, roadData):
	# Returns three lists, one with the roadData name travel
	#   one with the product of populations (beginning gravity
	#   analysis, can add multiple population sums and then 
	#   run analysis [Sum of Forces analysis])
	#   one with the distance data named distance
	#   All of the lists correspond to the same matrix points
	#   for each index of the list. 
	dim = len(pop.keys());
	# Find non-zero indices first, create shortlist
	travel = []
	gravitys = []
	distance = []
	for i in range(dim):
		for j in range(i, dim):
			if(dist[i][j] != 0):
				gravitys.append(pop[i][0]*pop[j][0]);
				travel.append(roadData[i][j])
				distance.append(dist[i][j])
	return [travel, gravitys, distance]

def runGravity(travel, gravitys, distance):
	# Start with population product in gravity matrix
	# Now run over beta values, divide by distance^beta
	#  Dumping values into a matrix with beta, K, R^2
	#  after regression with the travel data. 
	# Assuming desired regression orientation: Travel = m*Gravity + b
	analysis = np.zeros([20,4])
	for beta in np.arange(0.1, 2.1, .1):
		i = int(10*beta)
		gravityBeta = [(gravitys[x]/(distance[x]**beta)) for x in range(len(gravitys))]
		analysis[i-1][0] = beta;
		#analysis[i-1][1] = regressionNoIntercept(gravityBeta, travel)
		analysis[i-1][1], analysis[i-1][2] = regressionIntercept(gravityBeta, travel) 
		predicted = [(analysis[i-1][1]*x+analysis[i-1][2]) for x in gravityBeta]
		analysis[i-1][3] = rSquared(predicted, travel)
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
		x,y,z = formatRawMatrices(pop, dist, roadData);
		analysis = runGravity(x,y,z);
		print("[Beta, slope, intercept, R^2]")
		for line in analysis:
			print("[{:.3e}, {:.3e}, {:.3e}, {:.3e}]".format(line[0],line[1],line[2],line[3]))
		#pprint.pprint(analysis)
