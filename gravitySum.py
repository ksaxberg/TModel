import sys
from math import log
import pprint
import numpy as np
from gravity import *
import common
import parseData
DEBUG = common.DEBUG


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
    for i, distance in S.items():
        if (i != source and (source, i) not in memory and
                (i, source) not in memory):
            # Add this to memory then
            if i < source:
                memory[(i, source)] = [distance, PathSoFar[i]]
            else:
                memory[(source, i)] = [distance, PathSoFar[i]]
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
    # Make a copy of the matrix symmetric
    dist = np.array(distances)
    dist = dist + dist.T - np.diag(dist.diagonal())

    # Have spoiler route index -1
    size = len(dist[0])
    memory = {}
    for i in range(size):
        for j in range(i, size):
            runDijkstra(dist, i, j, memory)
    routeOverlap = [[[] for i in range(size)] for j in range(size)]
    for key, value in memory.items():
        # Suppose [City A, City D]
        # key is [A, D], value is [distance, [A, B, C, D]]
        # Where path A->D goes through specified edges
        length, path = value

        # Check if skip
        if common.useGravitySumThresh:
            # Remove from overlapping stuff here , skip over
            if common.deleteFromOriginalNetworkSum:
                # Removes edge if exceeds desired distance threshold
                if common.gravitySumDistThresh < length  or length < common.gravitySumDistThreshMinimum:
                    continue
            else:
                # Leaves original edges of graph intact
                if not len(path) == 2:
                    # Then have a pass-through edge
                    if common.gravitySumDistThresh < length  or length < common.gravitySumDistThreshMinimum:
                        continue

        for i in range(len(path)-1):
            # Store the fact that the parent route goes over edge,
            #  and total distance of the path.
            routeOverlap[min(path[i], path[i+1])][max(path[i], path[i+1])].append((key, length))
    if DEBUG:
        count = 0
        firstFive = []
        for i in range(len(routeOverlap)):
            for j in range(len(routeOverlap[0])):
                if (not routeOverlap[i][j]) and distances[i][j] != 0:
                    count += 1
                    firstFive.append((i, j, distances[i][j]))
        print("Count of routes not being used: {}".format(count))
        print("Route samples:")
        for i in range(min(5, len(firstFive))):
            print("\t{0}, {1}, {2}".format(firstFive[i][0], firstFive[i][1], firstFive[i][2]))

        with open("RoutesThatNeedChanging.txt", "w") as f:
            for i in range(len(firstFive)):
                f.write("{0}, {1}, {2}\n".format(firstFive[i][0], firstFive[i][1], firstFive[i][2]))

    return routeOverlap



def gravitySumOnEverything(pop, keys, distMatrix, roadData, retExample=False):
    # Helper function for gravity calculation
    def convertRoutesToList(overlaps, pops, beta, alpha):
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
                    # x = [[A, B], distance]
                    partialGravities[i][j] += ((pops[x[0][0]][0]*pops[x[0][1]][0])**alpha)/(x[1]**beta)
        return [x for x in partialGravities.flat if x != -1]

    # Making the distance matrix symmetric
    # Should already be upper triangular,
    # wrote overlap to not care about lower half
    overlap = overLappingRoutes(distMatrix)
    # Need to format into 3 lists, RoadData, Gravity, Distance
    # All indexed in order
    distMatrix = np.array(distMatrix)
    roadData = np.array(roadData)
    if common.useGravitySumThresh and common.deleteFromOriginalNetworkSum:
        # Remove components from roadDataList if not in overlap
        for i, row in enumerate(overlap):
            for j, cell in enumerate(row):
                if len(cell) == 0:
                    roadData[i][j] = 0
    roadDataList = [x for x in roadData.flat if x != 0]
    slopeValues = np.zeros([common.alphaSize(), common.betaSize()])
    interceptValues = np.zeros([common.alphaSize(), common.betaSize()])
    r2values = np.zeros([common.alphaSize(), common.betaSize()])
    matchR2 = 0
    exampleRow = []
    for i, alpha in enumerate(common.alphaIterate()):
        for j, beta in enumerate(common.betaIterate()):
            partialList = convertRoutesToList(overlap, pop, beta, alpha)

            slope, intercept, r2= common.singleRegression(partialList, roadDataList)
            if retExample:
                if not common.automaticBestMatch:
                    if np.isclose(alpha, common.alphaSumExample) and np.isclose(beta, common.betaSumExample):
                        exampleRow = partialList
                else:
                    if r2 > matchR2:
                        matchR2 = r2
                        exampleRow = partialList
            # Calculate prediction on current pathed values
            slopeValues[i][j] = slope
            interceptValues[i][j] = intercept
            r2values[i][j] = r2
    if retExample:
        return [slopeValues, interceptValues, r2values, exampleRow]
    else:
        return [slopeValues, interceptValues, r2values]
