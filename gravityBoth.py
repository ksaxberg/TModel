from gravity import gravityOnEverything as gravity
from gravitySum import gravitySumOnEverything as gravitySum
import sys
import parseData
from common import plotBoth


if __name__=="__main__":
    
    # From GravitySum

    pop = parseData.parsePopulation(sys.argv[1])
    keys = parseData.makeKeys(sys.argv[1])
    dist = parseData.parseEdges(sys.argv[2], keys, sumValues=False)
    distList = [i for i in dist.flat if i != 0]
    roadData = parseData.parseEdges(sys.argv[3], keys)
    roadDataList = [i for i in roadData.flat if i != 0]

    r2SumValues, interceptSumValues = gravitySum(pop, keys, dist, roadDataList)
    r2Values, interceptValues = gravity(pop, keys, dist, distList, roadDataList)
    # From Gravity
    plotBoth(roadDataList, r2Values, interceptValues, r2SumValues,
    interceptSumValues, titleString = " ")
