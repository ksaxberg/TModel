import sys
import math
import pprint
import numpy as np
from gravity import *
import common
import parseData
DEBUG = True


def formatMatrixAsList(someMatrix):
    # Assumption that matrix is square
    listy = []
    size = len(someMatrix[0])
    for i in range(size):
        for j in range(i, size):
            if (someMatrix[i][j] != 0):
                listy.append(someMatrix[i][j])
    return listy


def runDijkstra(distances, source, destination, memory):
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


def overLappingRoutes(distances):
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
    # Have spoiler route index -1
    size = len(distances[0])
    memory = {}
    for i in range(size):
        for j in range(i, size):
            # TODO: Sparse Matrix - run on edges, not vertex*vertex
            # Calculates how to get from A,B for every pair.
            runDijkstra(distances, i, j, memory)
    routeOverlap = [[[] for i in range(size)] for j in range(size)]
    for key, value in memory.items():
        # For each consecutive pair in the path
        # value is [S[i], PathSoFar[i]]
        for i in range(len(value[1])-1):
            if value[1][i] < value[1][i+1]:
                r1 = value[1][i]
                r2 = value[1][i+1]
            else:
                r2 = value[1][i]
                r1 = value[1][i+1]
            # Store the fact that the parent route goes over edge,
            #  and total distance of the path.
            routeOverlap[r1][r2].append((key, value[0]))
    return routeOverlap


def convertRoute(overlaps, pops, pop1, pop2, beta, alpha):
    if (pop2 > pop1):
        pop1, pop2 = pop2, pop1
    running = 0
    for path in overlaps[pop1][pop2]:
        if not path:
            continue
        for key, value in path:
            temp = (pops[key[0]]*pops[key[1]])**alpha
            temp /= value**beta
            running += temp
    return running


def convertRoutesToList(overlaps, pops, beta, alpha):
    # Constant factor K will have to be multiplied on the size
    partialGravities = np.zeros([len(overlaps), len(overlaps)])
    for i, row in enumerate(overlaps):
        for j, col in enumerate(row):
            if not col:
                continue
            for x in col:
                # For each x, add the partial gravity
                val = (pops[x[0][0]][0])*(pops[x[0][1]][0])
                val = val**alpha
                distance = x[1]**beta
                partialGravities[i][j] += val/distance
    return partialGravities


def gravitySum(pop, distances, roadData):
    # Making the distance matrix symmetric
    # Should already be upper triangular,
    # wrote overlap to not care about lower half
    overlap = overLappingRoutes(distances)
    # Need to format into 3 lists, RoadData, Gravity, Distance
    # All indexed in order
    roadDataList = [x for x in roadData.flat if (x != 0)]
    r2values = []
    interceptValues = []
    for alpha in common.alphaIterate():
        this_r2 = []
        this_intercept = []
        for beta in common.betaIterate():
            partialGravities = convertRoutesToList(overlap, pop, beta, alpha)
            partialList = [x for x in partialGravities.flat if (x != 0)]
            # partialList = formatMatrixAsList(partialGravities)
            # roadDataList = formatMatrixAsList(roadData)

            # Remove the common factor, reducing numerical error
            factor = min([math.log(j, 10) for j in partialList])
            partialList = [j/(10**factor) for j in partialList]

            slope, intercept = common.linRegress(partialList, roadDataList)
            # Calculate prediction on current pathed values
            this_intercept.append(math.log(abs(intercept), 10))
            predicted = [slope*x + intercept for x in partialList]
            r2 = common.rSquared(predicted, roadDataList)
            this_r2.append(r2)
            slope = slope / (10**factor)
            print("{:.3e}, {:.3e}, {:.3e}, {:.3e}, {:.3e}".format(beta, alpha,
                  slope, intercept, r2))
        r2values.append(this_r2)
        interceptValues.append(this_intercept)
    common.makePlot(roadDataList, r2values, interceptValues, 'GravitySum', '{} Gravity Sum'.format(sys.argv[1].split('/')[0]))


def gravitySumOnEverything(pop, keys, distMatrix, roadDataList):
    # Making the distance matrix symmetric
    # Should already be upper triangular,
    # wrote overlap to not care about lower half
    overlap = overLappingRoutes(distMatrix)
    # Need to format into 3 lists, RoadData, Gravity, Distance
    # All indexed in order
    r2values = []
    interceptValues = []
    for alpha in common.alphaIterate():
        this_r2 = []
        this_intercept = []
        for beta in common.betaIterate():
            partialGravities = convertRoutesToList(overlap, pop, beta, alpha)
            partialList = [x for x in partialGravities.flat if (x != 0)]
            # partialList = formatMatrixAsList(partialGravities)
            # roadDataList = formatMatrixAsList(roadData)

            # Remove the common factor, reducing numerical error
            factor = min([math.log(j, 10) for j in partialList])
            partialList = [j/(10**factor) for j in partialList]

            slope, intercept = common.linRegress(partialList, roadDataList)
            # Calculate prediction on current pathed values
            this_intercept.append(math.log(abs(intercept), 10))
            predicted = [slope*x + intercept for x in partialList]
            r2 = common.rSquared(predicted, roadDataList)
            this_r2.append(r2)
            slope = slope / (10**factor)
        r2values.append(this_r2)
        interceptValues.append(this_intercept)
    return [r2values, interceptValues]


if __name__ == '__main__' and (len(sys.argv) == 4):
        # Matrix Form
        # pop = parseData.parsePopulation(sys.argv[1])
        # dist = parseData.parseDistance(sys.argv[2])
        # roadData = parseData.parseDistance(sys.argv[3])
        # gravitySum(pop, dist, roadData)

        # Edgewise Form, simply builds matrices for now
        pop = parseData.parsePopulation(sys.argv[1])
        keys = parseData.makeKeys(sys.argv[1])
        dist = parseData.parseEdges(sys.argv[2], keys)
        roadData = parseData.parseEdges(sys.argv[3], keys)
        print("{}\nGravity Sum\n{}\n".format("-"*25, "-"*25))
        print("Beta, Alpha, Slope, Intercept, R^2")
        gravitySum(pop, dist, roadData)
