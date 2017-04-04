from matplotlib import cm
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import gridspec
from matplotlib import rcParams
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import math

class Network:
    alphaMin = 0.1
    alphaMax = 3
    alphaExample = .5 
    betaMin = 0.1 
    betaMax = 3
    betaExample = 0.1 
    stepValueAlpha = 0.1
    stepValueBeta = 0.1

    def __init__(self, popFile, distanceFile, roadFile):
        # Assuming edge-wise representation
        self.pop = parsePopulation(popFile)
        self.keys = makeKeys(self.pop)
        self.dist = parseEdges(distanceFile, self.keys)
        self.distList = [i for i in self.dist.flat if i != 0]
        self.roadData = parseEdges(roadFile, self.keys)
        self.roadDataList = [i for i in self.roadData.flat if i != 0]
        __doRun();

    def  __doRun():
        ### Example run
        gravityList = __makeGravityList(self.pop, self.dist)
        gravityEstimate = [x**Network.alphaExample/(distList[i]**Network.betaExample) for i, x in enumerate(gravityList)]
        exampleRow = gravityEstimate
        m, b, _ = singleRegression(exampleRow, roadDataList)
        ####    End
    
        self.r2SumValues, self.interceptSumValues = __gravitySum(self.pop, self.keys, self.dist, self.roadDataList)
        self.r2Values, self.interceptValues = __gravityOnEverything(self.pop, self.keys, self.dist, self.distList, self.roadDataList)
        # From Gravity
        __plotBoth(roadDataList, r2Values, interceptValues, r2SumValues,
            interceptSumValues, titleString = " ", rowExampleGravity=exampleRow,
            rowslope=m, rowint=b)
    

    def __makeGravityList(pop, dist):
        """ Creates a list of population products
    
        Takes the population and distance matrices, creates the matrix
        of distance products for each non-zero entry in the distance matrix.
        Returns the list of such a matrix.
        """
        # FROM GRAVITY
        dim = len(pop.keys())
        # Find non-zero indices first, create shortlist
        gravitys = np.zeros([dim, dim])
        for i in range(dim):
            for j in range(i, dim):
                if(dist[i][j] != 0):
                    gravitys[i][j] = pop[i][0]*pop[j][0]
        # is the same as the above in terms of element ordering
        gravityList = [i for i in gravitys.flat if i != 0]
        return gravityList


    def __runGravity(travel, gravitys, distance, alpha=1):
        """ Start with population product in gravity matrix
    
        Now run over beta values, divide by distance^beta
        Dumping values into a matrix with beta, K, R^2
        after regression with the travel data.
        Assuming desired regression orientation: Travel = m*Gravity + b
        """
        # FROM GRAVITY
        M = np.zeros([common.numBetaEntries(), 5])
        for i, beta in enumerate(common.betaIterate()):
            gravityBeta = [(x**alpha/(distance[j]**beta)) for j, x
                           in enumerate(gravitys)]
            factor = min([math.log(j, 10) for j in gravityBeta])
            gravityBeta = [j/(10**factor) for j in gravityBeta]
            M[i][0], M[i][1] = beta, alpha
            slope, M[i][3] = common.linRegress(gravityBeta, travel)
            M[i][2] = slope / (10**factor) 
            predicted = [slope*x+M[i][3] for x in gravityBeta]
            M[i][4] = common.rSquared(predicted, travel)
        return M


    def __gravityOnEverything(pop, keys, distMatrix, distList, roadDataList):
        # FROM GRAVITY
        gravityList = __makeGravityList(pop, distMatrix)
        
        r2values = []
        interceptValues = []
        for alpha in common.alphaIterate():
            analysis = __runGravity(roadDataList, gravityList, distList, alpha)
            this_r2 = []
            this_intercept = []
            for line in analysis:
                this_r2.append(line[4])
                this_intercept.append(math.log(abs(line[3]), 10))
            r2values.append(this_r2)
            interceptValues.append(this_intercept)
        return [r2values, interceptValues]

    def __singleRegression(x, y):
        """
        Runs through a single regression, assuming that the gravity values 
        are calculated with alpha and beta already
        """
        slope, intercept = __linRegress(x, y)
        predicted = [slope*i+intercept for i in x]
        r2 = common.rSquared(predicted, y)
        return slope, intercept, r2

#####################################################################
    # From PARSEDATA.PY
#####################################################################

    def __parseEdges(filename, keys, sumValues=True):
        """ Parses Edges file into numpy matrix
    
        Takes an edge-wise file representation of data, and using a keyset
        from population.txt (which must have been parsed first), creates
        a numpy matrix, upper triangular, indexed by those keys.
        The sumValues keyflag allows the user to indicate whether the edgewise
        representation contains duplicates that should be added, sumValues=False,
        or that should be ignored, sumValues=True. Default is True, only the first
        value encountered will be used for each pair.
        Note: No edge-wise pair may have a value of zero.
        """
        matrix = np.zeros([len(keys), len(keys)])
        with open(filename) as f:
            # Assuming each line is sumValues
            for line in f:
                place1, place2, value = line.strip().split(',')
                ind1 = keys[place1.strip()]
                ind2 = keys[place2.strip()]
                # Make ind1 the smaller, upper triang matrix
                if ind1 > ind2:
                    ind1, ind2 = ind2, ind1
                if not sumValues and matrix[ind1][ind2] == 0:
                    matrix[ind1][ind2] = float(value.strip())
                elif sumValues:
                    matrix[ind1][ind2] += float(value.strip())
        return matrix


    def __makeKeys(filename):
        """ Makes city->index keys for Edge parsing from population.txt file
    
        Population.txt must be csv, first item is city, second is population.
        This parses the csv into a keylist, allowing for transitioning from
        city names into indexes. Assuming edgewise representation contains
        full match pairs for keys.
        """
        # Assuming working with the population file
        d = {}
        with open(filename) as f:
            for i, line in enumerate(f):
                key = line.strip().split(',')[0].strip()
                d[key] = i
        return d


    def __parsePopulation(filename):
        """ Makes a dictionary of city, population pairs in population.txt
    
        Dictionary is in the form index -> [population, cityname]
        """
        d = {}
        with open(filename) as f:
            for i, line in enumerate(f):
                temp = line.strip().split(',')
                d[i] = [float(temp[1].strip()), temp[0].strip()]
        return d

#####################################################################
    # From GRAVITYSUM.PY
#####################################################################
    def __runDijkstra(distances, source, destination, memory):
        """
        Distances is a formatted, symmetric matrix (assuming undirected graph)
         0 indicates no edge presences
         Naive implementation of Dijkstras, not for efficiency
         distances[0] should retrieve row 0, indicating distance from 0 to
         every other point.
         symmetric matrix allows for starting with distance[i]
        """
        if (source, destination) in memory:
            return memory[(source, destination)]
        if (destination, source) in memory:
            return memory[(destination, source)]
        # S is colleciton of shortest decided distances already
        S = {source: 0}
        PathSoFar = {source: [source]}
        D = {i: distances[source][i] for i in range(len(distances[0]))
             if distances[source][i] != 0}
        # Skipping non-connected graphs, where no path from source
        if not D:
            return
        for key, value in D.items():
            PathSoFar[key] = [source, key]
        while destination not in S.keys():
            if not D:
                # If D empty, not connected. No Path between them.
                return
            # End skipping
            minim = min(D.values())
            newMin = [key for key, value in D.items() if value == minim]
            newMin = newMin[0]
            # Dealing with newMin item. (node, distance)
            S[newMin] = minim
            del D[newMin]
            distFromNew = distances[newMin]
            for key, value in D.items():
                # Replace all distances that need replacing
                if distFromNew[key] != 0 and value > minim + distFromNew[key]:
                    newValue = minim + distFromNew[key]
                    D[key] = newValue
                    # Replace path with newly found shorter one
                    PathSoFar[key] = list(PathSoFar[newMin])
                    PathSoFar[key].append(key)
            for x in range(len(distances[0])):
                if x in S.keys() or distFromNew[x] == 0:
                    continue
                # For nonfinished indices
                elif x not in D.keys():
                    D[x] = distFromNew[x]+minim
                    # Add paths for newly found elements
                    PathSoFar[x] = list(PathSoFar[newMin])
                    PathSoFar[x].append(x)
        # Only adding completed routes to the memory, things in S
        for i in S.keys():
            if (i != source and (source, i) not in memory and
                    (i, source) not in memory):
                # Add this to memory then
                if i < source:
                    memory[(i, source)] = [S[i], PathSoFar[i]]
                else:
                    memory[(source, i)] = [S[i], PathSoFar[i]]
        return
    
    def __makeMatrixSymmetric(matrix):
        return matrix + matrix.T - np.diag(matrix.diagonal()) 
    
    def __overLappingRoutes(distances):
        """ Runs the dijkstra algorithm on all route pairs, returns the overlap
    
        Input: a matrix of distances between city pairs, upper triangular form.
        This function utilizes a memory tool to shorten dijkstra running time,
        though it does not improve algorithmic efficiency. The routes are then
        parsed, and the return output has a collection of the type:
        routeOverlap[i][j]=>[..., ((parent1, parent2), distance),...]
        Where we know that every value in the list is a pair of parents whose
        shortest path goes over the current city connection of interest, ie
        connection i, j.
        """
        dist = __makeMatrixSymmetric(distances)
        # Have spoiler route index -1
        size = len(dist[0])
        memory = {}
        for i in range(size):
            for j in range(i, size):
                # Sparse Matrix - run on edges, not vertex*vertex
                # Can't do that, miss routes
                # Calculates how to get from A,B for every pair.
                #if dist[i][j] != 0:
                __runDijkstra(dist, i, j, memory)
        routeOverlap = [[[] for i in range(size)] for j in range(size)]
        for key, value in memory.items():
            # For each consecutive pair in the path
            # value is [S[i], PathSoFar[i]]
            for i in range(len(value[1])-1):
                r1 = min(value[1][i], value[1][i+1])
                r2 = max(value[1][i], value[1][i+1])
                # Store the fact that the parent route goes over edge,
                #  and total distance of the path.
                routeOverlap[r1][r2].append((key, value[0]))
        #TODO: Remove count of routes
        if self.DEBUG:
            count = 0
            firstFive = []
            for i in range(len(routeOverlap)):
                for j in range(len(routeOverlap[0])):
                    if routeOverlap[i][j]:
                        count += 1
                    elif distances[i][j] != 0:
                        firstFive.append((i, j, distances[i][j]))
            print("Count of overlapping routes returned: {}".format(count))
            print("Route samples:")
            for i in range(min(5, len(firstFive))):
                print("\t{0}, {1}, {2}".format(firstFive[i][0], firstFive[i][1], firstFive[i][2]))
            
            with open("RoutesThatNeedChanging.txt", "w") as f:
                for i in range(len(firstFive)):
                    f.write("{0}, {1}, {2}\n".format(firstFive[i][0], firstFive[i][1], firstFive[i][2]))
                
        return routeOverlap
    
    
    def __convertRoutesToList(overlaps, pops, beta, alpha):
        # Constant factor K will have to be multiplied on the size
        partialGravities = np.ones([len(overlaps), len(overlaps)])
        partialGravities *= -1
        for i, row in enumerate(overlaps):
            for j, col in enumerate(row):
                if not col:
                    continue
                else:
                    # Reset to zero if have values to add
                    partialGravities[i][j] = 0
                for x in col:
                    # For each x, add the partial gravity
                    val = (pops[x[0][0]][0])*(pops[x[0][1]][0])
                    val = val**alpha
                    distance = x[1]**beta
                    partialGravities[i][j] += val/distance
        return partialGravities
    
   """ 
    def __gravitySum(pop, distances, roadData):
        # Making the distance matrix symmetric
        # Should already be upper triangular,
        # wrote overlap to not care about lower half
        overlap = __overLappingRoutes(distances)
        # Need to format into 3 lists, RoadData, Gravity, Distance
        # All indexed in order
        roadDataList = [x for x in roadData.flat if (x != 0)]
        r2values = []
        interceptValues = []
        for alpha in __alphaIterate():
            this_r2 = []
            this_intercept = []
            for beta in __betaIterate():
                partialGravities = __convertRoutesToList(overlap, pop, beta, alpha)
                partialList = [x for x in partialGravities.flat if x != -1]
    
                # Remove the common factor, reducing numerical error
                #factor = min([math.log(j, 10) for j in partialList])
                #partialList = [j/(10**factor) for j in partialList]
    
                slope, intercept = __linRegress(partialList, roadDataList)
                # Calculate prediction on current pathed values
                this_intercept.append(math.log(abs(intercept), 10))
                predicted = [slope*x + intercept for x in partialList]
                r2 = __rSquared(predicted, roadDataList)
                this_r2.append(r2)
                #slope = slope / (10**factor)
                print("{:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}".format(beta, alpha,
                      slope, intercept, r2))
            r2values.append(this_r2)
            interceptValues.append(this_intercept)
        common.makePlot(roadDataList, r2values, interceptValues, 'GravitySum', '{} Gravity Sum'.format(sys.argv[1].split('/')[0]))
    """
    
    def __gravitySumOnEverything(pop, keys, distMatrix, roadDataList):
        # Making the distance matrix symmetric
        # Should already be upper triangular,
        # wrote overlap to not care about lower half
        overlap = __overLappingRoutes(distMatrix)
        # Need to format into 3 lists, RoadData, Gravity, Distance
        # All indexed in order
        r2values = []
        interceptValues = []
        for alpha in __alphaIterate():
            this_r2 = []
            this_intercept = []
            for beta in __betaIterate():
                partialGravities = __convertRoutesToList(overlap, pop, beta, alpha)
                partialList = [x for x in partialGravities.flat if x != -1]
    
                # Remove the common factor, reducing numerical error
                #factor = min([math.log(j, 10) for j in partialList])
                #partialList = [j/(10**factor) for j in partialList]
    
                if self.DEBUG: print("Length of partial: {}\nLength of roadDataList: {}".format(len(partialList), len(roadDataList)))
                slope, intercept = __linRegress(partialList, roadDataList)
                # Calculate prediction on current pathed values
                this_intercept.append(math.log(abs(intercept), 10))
                predicted = [slope*x + intercept for x in partialList]
                r2 = __rSquared(predicted, roadDataList)
                this_r2.append(r2)
                #slope = slope / (10**factor)
            r2values.append(this_r2)
            interceptValues.append(this_intercept)
        return [r2values, interceptValues]
#####################################################################
    # From COMMON.PY
#####################################################################
    def __alphaIterate():
        return np.arange(alphaMin, alphaMax, stepValueAlpha)
    
    def __betaIterate():
        return np.arange(betaMin, betaMax, stepValueBeta)
    
    def __numBetaEntries():
        return int(math.ceil((betaMax-betaMin)/stepValueBeta))
    
    def __formatScientific(x):
        return "{:.2E}".format(Decimal(x))
    
    def __rSquared(pred, meas):
        """ Calculate r^2 value.
    
        Calculates r^2 between predicted and measured data values.
        Measured value must be second argument.
        """
        # sum(pred - meas)^2
        # divided by sum(pred - mean)^2
        mean = sum(meas)/len(meas)
        meanError = sum([(meas[i] - mean)**2 for i in range(len(pred))])
        sqrError = sum([(pred[i]-meas[i])**2 for i in range(len(pred))])
        return 1-sqrError/meanError

    def __linRegress(x, y):
        """ Calculate the regression of x, y
    
        Uses numpy's linalg.lstsq method to calculate a regression, returning
        slope, intercept
        """
        x_values = np.array(x)
        y_values = np.array(y)
        if DEBUG:
            print("x length: {}\ny length: {}\n".format(len(x), len(y)))
        A = np.vstack([x_values, np.ones(len(x_values))]).T
        slope, intercept = np.linalg.lstsq(A, y_values)[0]
        return slope, intercept

    def __plotBoth(roadDataList, z, intercept, zSum, interceptSum, name="img", titleString="", rowExampleGravity=[], rowslope=0, rowint=0):
        """ Makes four countour plots, box plot and saves to the specified filename
    
        File will be saved into current directory as a png, input matrix z must
        be of the size [xval, yval] as indicated
        """
        #rcParams.update({'font.size': 7, 'xtick.labelsize': 4 })
        rcParams.update({'font.size': 7})
    
        xval = __betaIterate()
        yval = __alphaIterate()
        fig = plt.figure(figsize=(10, 10), dpi=200)
        #fig.set_size_inches(5, 5)
        gs = gridspec.GridSpec(6, 4)
        
        #### First Row Option 1: Single large boxplot
        #box1 = fig.add_subplot(gs[0,:])
        #box1.boxplot(roadDataList, 0, 'rs', 0)
        #box1.set_xlabel('Traffic Data Range')
        ####    End 
    
        #### First Row Option 2: Boxplot and plot of alpha1, beta 1
        if not rowExampleGravity:
            raise ValueError("Plot wants to show Alpha={}, Beta={} gravity regression but regression values not passed in as rowA1B1ofGravity".format(self.alphaExample, self.betaExample))
        box1 = fig.add_subplot(gs[0, 0:2])
        box1.boxplot(roadDataList, 0, 'rs', 0)
        box1.set_xlabel('Traffic Data Range')
        
        scatter = fig.add_subplot(gs[0:2, 2:])
        m = rowslope
        b = rowint
        predictions = [x*m + b for x in rowExampleGravity]
        factor = 1
        for i in range(len(predictions)):
            factor = max(factor, predictions[i], rowExampleGravity[i])
        scatter.scatter(rowExampleGravity, predictions, c='b', marker='x', label="predictions")
        scatter.scatter(rowExampleGravity, roadDataList, c='r', marker='+', label="actual") 
        scatter.set_xlabel('Gravity Val input')
        scatter.set_ylim(1, factor*10)
        scatter.set_yscale('log')
        scatter.set_xscale('log')
        scatter.set_title("Gravity where alpha={}, beta={} \nm={} b={}".format(alphaExample, betaExample,
                          formatScientific(m), formatScientific(b)))
        scatter.set_ylabel('Number of People')
        scatter.legend(loc="upper left", frameon=False)
        ####    End
    
        # Gravity Slope
        sub1 = fig.add_subplot(gs[2:4, 0:2])
        norm = colors.Normalize(0, 1.01)
        cmap = cm.get_cmap('nipy_spectral', 100)
        # arange of the following is partial setup for colorbar
        CS = sub1.contourf(xval, yval, z, np.arange(0, 1.01, .01),
                         cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
        sub1.set_xlabel('Beta')
        sub1.set_ylabel('Alpha')
        if titleString:
            sub1.set_title(titleString+' R^2 Values')
        plt.colorbar(CS, )
    
    
        # Gravity Intercept
        sub2 = fig.add_subplot(gs[2:4,2:])
        norm = colors.Normalize(0, 10)
        cmap = cm.get_cmap('nipy_spectral', 100)
        # arange of the following is partial setup for colorbar
        CS = sub2.contourf(xval, yval, intercept, np.arange(0, 10, 0.1),
                         cmap=cmap, norm=norm,  vmin=0, vmax=10)
        sub2.set_xlabel('Beta')
        sub2.set_ylabel('Alpha')
        if titleString:
            sub2.set_title(titleString+' Intercept Values log10')
        plt.colorbar(CS, )
    
    
        # Gravity Sum Slope
        sub3 = fig.add_subplot(gs[4:6,0:2])
        norm = colors.Normalize(0, 1.01)
        cmap = cm.get_cmap('nipy_spectral', 100)
        # arange of the following is partial setup for colorbar
        CS = sub3.contourf(xval, yval, zSum, np.arange(0, 1.01, .01),
                         cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
        sub3.set_xlabel('Beta')
        sub3.set_ylabel('Alpha')
        if titleString:
            sub3.set_title(titleString+' Sum R^2 Values')
        plt.colorbar(CS, )
    
    
        # Gravity Sum Intercept
        sub4 = fig.add_subplot(gs[4:6,2:])
        norm = colors.Normalize(0, 10)
        cmap = cm.get_cmap('nipy_spectral', 100)
        # arange of the following is partial setup for colorbar
        CS = sub4.contourf(xval, yval, interceptSum, np.arange(0, 10, 0.1),
                         cmap=cmap, norm=norm,  vmin=0, vmax=10)
        sub4.set_xlabel('Beta')
        sub4.set_ylabel('Alpha')
        if titleString:
            sub4.set_title(titleString+' Sum Intercept Values log10')
        plt.colorbar(CS, )
    
        # Update Change space between subplots, save image
        gs.update(wspace=1, hspace=1)
        if name[-4:] != '.png':
            #fig.savefig(name+'.png', bbox_inches='tight')
            fig.savefig(name+'.png', dpi=900)
        else:
            fig.savefig(name)
