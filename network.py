
class Network:

    def __init__(self, popFile, distanceFile, roadFile):
        # Assuming edge-wise representation
        this.pop = parsePopulation(popFile)
        this.keys = makeKeys(this.pop)
        this.dist = parseEdges(distanceFile, this.keys)
        this.roadData = parseEdges(roadFile, this.keys)

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


    def runGravity(travel, gravitys, distance, alpha=1):
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


    def gravityOnEverything(pop, keys, distMatrix, distList, roadDataList):
        # FROM GRAVITY
        gravityList = formatRawMatrices(pop, distMatrix)
        
        r2values = []
        interceptValues = []
        for alpha in common.alphaIterate():
            analysis = runGravity(roadDataList, gravityList, distList, alpha)
            this_r2 = []
            this_intercept = []
            for line in analysis:
                this_r2.append(line[4])
                this_intercept.append(math.log(abs(line[3]), 10))
            r2values.append(this_r2)
            interceptValues.append(this_intercept)
        return [r2values, interceptValues]


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
