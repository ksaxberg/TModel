import numpy as np
import sys
import parseData
import common


def formatRawMatrices(pop, dist):
    """ Creates a list of population products

    Takes the population and distance matrices, creates the matrix
    of distance products for each non-zero entry in the distance matrix.
    Returns the list of such a matrix.
    """
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
    M = np.zeros([common.numBetaEntries(), 5])
    for i, beta in enumerate(common.betaIterate()):
        gravityBeta = [(x**alpha/(distance[j]**beta)) for j, x
                       in enumerate(gravitys)]
        M[i][0], M[i][1] = beta, alpha
        M[i][2], M[i][3] = common.linRegress(gravityBeta, travel)
        predicted = [(M[i][2]*x+M[i][3]) for x in gravityBeta]
        M[i][4] = common.rSquared(predicted, travel)
    return M


if __name__ == '__main__' and len(sys.argv) == 4:
    """
    Runs the basic gravity law analysis on the data given, from files
    whose names are command line arguments.
    """
    # Matrix Form
    # pop = parseData.parsePopulation(sys.argv[1])
    # dist = parseData.parseDistance(sys.argv[2])
    # roadData = parseData.parseDistance(sys.argv[3])
    # Edgewise form
    pop = parseData.parsePopulation(sys.argv[1])
    keys = parseData.makeKeys(sys.argv[1])

    dist = parseData.parseEdges(sys.argv[2], keys)
    distList = [i for i in dist.flat if i != 0]

    roadData = parseData.parseEdges(sys.argv[3], keys)
    roadDataList = [i for i in roadData.flat if i != 0]

    gravityList = formatRawMatrices(pop, dist)

    print("{}\nGravity\n{}\n".format("-"*25, "-"*25))
    print("Beta, alpha, slope, intercept, R^2")
    zvalues = []
    for alpha in common.alphaIterate():
        analysis = runGravity(roadDataList, gravityList, distList, alpha)
        this_z = []
        for line in analysis:
            this_z.append(line[4])
            print("{:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}".format(
                  line[0], line[1], line[2], line[3], line[4]))
        zvalues.append(this_z)
    common.makePlot(zvalues, 'Gravity', 'Basic Gravity R^2 Values')
