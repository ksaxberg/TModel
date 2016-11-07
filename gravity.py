# Runs a basic gravity law analysis, given the population table and distance table
import numpy as np
from matplotlib import cm
from matplotlib import colors
from matplotlib import colorbar
import matplotlib.pyplot as plt
import sys
import parseData
import constants

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

def runGravity(travel, gravitys, distance, alpha=1):
	# Start with population product in gravity matrix
	# Now run over beta values, divide by distance^beta
	#  Dumping values into a matrix with beta, K, R^2
	#  after regression with the travel data. 
	# Assuming desired regression orientation: Travel = m*Gravity + b
	analysis = np.zeros([int(10*constants.betaMax-constants.betaMin),5])
	for beta in np.arange(constants.betaMin, constants.betaMax, .1):
		i = int(10*beta)
		gravityBeta = [(gravitys[x]**alpha/(distance[x]**beta)) for x in range(len(gravitys))]
		analysis[i-1][0] = beta;
		analysis[i-1][1] = alpha;
		analysis[i-1][2], analysis[i-1][3] = regressionIntercept(gravityBeta, travel) 
		predicted = [(analysis[i-1][2]*x+analysis[i-1][3]) for x in gravityBeta]
		analysis[i-1][4] = rSquared(predicted, travel)
	return analysis
		

def regressionIntercept(x, y):
	x_values = np.array(x)
	y_values = np.array(y)
	A = np.vstack([x_values, np.ones(len(x_values))]).T
	slope, intercept = np.linalg.lstsq(A,y_values)[0]
	return [slope, intercept]

def rSquared(predicted, actual):
	# sum(predicted - actual)^2
	# divided by sum(predicted - mean)^2
	mean = sum(actual)/len(actual)
	meanError = sum([(actual[i] - mean)**2 for i in range(len(predicted))])
	sqrError = sum([(predicted[i]-actual[i])**2 for i in range(len(predicted))])
	return 1-sqrError/meanError
	
if __name__ == '__main__':
	if(len(sys.argv) == 4):
		# Matrix Form
		#pop = parseData.parsePopulation(sys.argv[1]);
		#dist = parseData.parseDistance(sys.argv[2]);
		#roadData = parseData.parseDistance(sys.argv[3]);
		# Edgewise form
		pop = parseData.parsePopulation(sys.argv[1])
		keys = parseData.makeKeys(sys.argv[1])
		dist = parseData.parseEdges(sys.argv[2], keys)
		roadData = parseData.parseEdges(sys.argv[3], keys)
		x,y,z = formatRawMatrices(pop, dist, roadData);
		print("{}\nGravity\n{}\n".format("-"*25, "-"*25))
		print("Beta, alpha, slope, intercept, R^2")
		zvalues = []
		for alpha in np.arange(constants.alphaMin, constants.alphaMax, .1):
			analysis = runGravity(x,y,z,alpha);
			this_z = []
			for line in analysis:
				this_z.append(line[4])
				print("{:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}".format(
				line[0],line[1],line[2],line[3],line[4]))
			zvalues.append(this_z)
		#Build a plot of the z values
		xval = np.arange(constants.betaMin, constants.betaMax, .1)
		yval = np.arange(constants.alphaMin, constants.alphaMax, .1)

		#fig = plt.figure()
		#ax = fig.add_subplot(111)
		fig, ax = plt.subplots(1,1,)
		norm = colors.Normalize(0, 1.05)
		cmap = cm.get_cmap('coolwarm', 10)
		CS = ax.contourf(xval, yval, zvalues, np.arange(0,1.05, .05), 
				cmap=cmap, norm=norm,  vmin=0, vmax=1.05)
		ax.set_xlabel('Beta')
		ax.set_ylabel('Alpha')
		plt.title('Basic Gravity Regression Values')
		plt.colorbar(CS,)
		fig.savefig('Gravity.png', bbox_inches='tight')
		#plt.show()
