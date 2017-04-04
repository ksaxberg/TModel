import numpy as np
import math
import sys
import parseData
import common


def gravityOnEverything(pop, keys, distMatrix, distList, roadDataList):
    """ Creates a list of population products
    
    Takes the population and distance matrices, creates the matrix
    of distance products for each non-zero entry in the distance matrix.
    Returns the list of such a matrix.
    """
    dim = len(pop.keys())
    # Find non-zero indices first, create shortlist
    popProd = np.ones([dim, dim])
    popProd *= -1
    for i in range(dim):
        for j in range(i, dim):
            if distMatrix[i][j] != 0:
                popProd[i][j] = pop[i][0]*pop[j][0]
    # is the same as the above in terms of element ordering
    popProdList = [i for i in popProd.flat if i != -1] 
    
    slopeValues = np.zeros([common.alphaSize(), common.betaSize()]) 
    interceptValues = np.zeros([common.alphaSize(), common.betaSize()]) 
    r2values = np.zeros([common.alphaSize(), common.betaSize()]) 

    for i, alpha in enumerate(common.alphaIterate()):
        for j, beta in enumerate(common.betaIterate()):
            gravityBeta = [x**alpha/(distList[k]**beta) for k, x
                           in enumerate(popProdList)]
            slope, intercept, r2= common.singleRegression(gravityBeta, roadDataList)
            slopeValues[i][j] = slope
            interceptValues[i][j] = intercept
            r2values[i][j] = r2

    return [slopeValues, interceptValues, r2values]
