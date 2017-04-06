from gravity import gravityOnEverything as gravity
from gravitySum import gravitySumOnEverything as gravitySum
import sys
import parseData
import common
import numpy as np

def gravityBoth(popFile, distFile, roadFile, titleString = " "):
    pop = parseData.parsePopulation(popFile)
    keys = parseData.makeKeys(popFile)
    dist = parseData.parseEdges(distFile, keys, sumValues=False)
    distList = [i for i in dist.flat if i != 0]
    roadData = parseData.parseEdges(roadFile , keys)
    roadDataList = [i for i in roadData.flat if i != 0]
    if common.DEBUG:
        print("Length of pop:{}\n\tof dist:{}\n\tof distList:{}\n\tof roadData:{}\n\tof roadDataList:{}".format(len(pop), len(dist), len(distList), len(roadData), len(roadDataList)))


    slopeSumValues, interceptSumValues, r2SumValues , gravitySumEstimate= gravitySum(pop, keys, np.array(dist), np.array(roadData), retExample = True)
    slopeValues, interceptValues, r2Values, gravityEstimate = gravity(pop, keys, dist, distList, np.array(roadDataList), retExample=True)
    # From Gravity
    common.plotBoth(roadDataList, 
        r2Values, 
        interceptValues, 
        r2SumValues,
        interceptSumValues, 
        titleString = titleString, 
        rowExampleGravity=gravityEstimate,
        rowExampleSumGravity=gravitySumEstimate)

if __name__=="__main__":
    # From GravitySum
    gravityBoth(sys.argv[1], sys.argv[2], sys.argv[3])
