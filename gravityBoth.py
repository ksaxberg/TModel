from gravity import gravityOnEverything as gravity
from gravity import formatRawMatrices as formatMatrix
from gravity import singleRegression
from gravitySum import gravitySumOnEverything as gravitySum
import sys
import parseData
import common


if __name__=="__main__":
    
    # From GravitySum

    pop = parseData.parsePopulation(sys.argv[1])
    keys = parseData.makeKeys(sys.argv[1])
    dist = parseData.parseEdges(sys.argv[2], keys, sumValues=False)
    distList = [i for i in dist.flat if i != 0]
    roadData = parseData.parseEdges(sys.argv[3], keys)
    roadDataList = [i for i in roadData.flat if i != 0]

    #### Simply to get a1b1Row for plotting alpha 1, beta 1
    gravityList = formatMatrix(pop, dist)
    gravityEstimate = [x**common.alphaExample/(distList[i]**common.betaExample) for i, x in enumerate(gravityList)]
    exampleRow = gravityEstimate
    m, b, _ = singleRegression(exampleRow, roadDataList)
    ####    End

    r2SumValues, interceptSumValues = gravitySum(pop, keys, dist, roadDataList)
    r2Values, interceptValues = gravity(pop, keys, dist, distList, roadDataList)
    # From Gravity
    common.plotBoth(roadDataList, r2Values, interceptValues, r2SumValues,
        interceptSumValues, titleString = " ", rowExampleGravity=exampleRow,
        rowslope=m, rowint=b)
    #plotBoth(roadDataList, r2Values, interceptValues, r2SumValues, interceptSumValues, titleString = " ")
