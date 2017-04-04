from gravity import gravityOnEverything as gravity
from gravitySum import gravitySumOnEverything as gravitySum
import sys
import parseData
import common
import numpy as np


if __name__=="__main__":
    
    # From GravitySum

    pop = parseData.parsePopulation(sys.argv[1])
    keys = parseData.makeKeys(sys.argv[1])
    dist = parseData.parseEdges(sys.argv[2], keys, sumValues=False)
    distList = [i for i in dist.flat if i != 0]
    roadData = parseData.parseEdges(sys.argv[3], keys)
    roadDataList = [i for i in roadData.flat if i != 0]
    if common.DEBUG:
        print("Length of pop:{}\n\tof dist:{}\n\tof distList:{}\n\tof roadData:{}\n\tof roadDataList:{}".format(len(pop), len(dist), len(distList), len(roadData), len(roadDataList)))

    #### Simply to get a1b1Row for plotting alpha 1, beta 1
    dim = len(pop.keys())
    # Find non-zero indices first, create shortlist
    popProd = np.ones([dim, dim])
    popProd *= -1
    for i in range(dim):
        for j in range(i, dim):
            if dist[i][j] != 0:
                popProd[i][j] = pop[i][0]*pop[j][0]
    # is the same as the above in terms of element ordering
    popProdList = [i for i in popProd.flat if i != -1] 
    
    gravityEstimate = [(x**common.alphaExample)/(distList[i]**common.betaExample) for i, x in enumerate(popProdList)]
    m, b, r2 = common.singleRegression(gravityEstimate, roadDataList)
    ####    End

    slopeSumValues, interceptSumValues, r2SumValues = gravitySum(pop, keys, np.array(dist), np.array(roadData))
    slopeValues, interceptValues, r2Values = gravity(pop, keys, dist, distList, np.array(roadDataList))
    # From Gravity
    common.plotBoth(roadDataList, r2Values, interceptValues, r2SumValues,
        interceptSumValues, titleString = " ", rowExampleGravity=gravityEstimate,
        rowslope=m, rowint=b)
