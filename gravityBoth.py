from gravity import gravityOnEverything as gravity
from gravitySum import gravitySumOnEverything as gravitySum
from gravitySum_ContribRegress import gravitySumOnEverything as gravitySumContrib
import sys
import parseData
import common
import numpy as np

def gravityBoth(popFile, distFile, roadFile, titleString = " ", filename="img"):
    pop = parseData.parsePopulation(popFile)
    keys = parseData.makeKeys(popFile)
    dist = parseData.parseEdges(distFile, keys, sumValues=False)
    distList = [i for i in dist.flat if i != 0]
    if common.useErrorBound:
        roadData, minimData, maximData = parseData.parseEdges(roadFile , keys, errorBounds=True)
        roadDataList = [i for i in roadData.flat if i != 0]
        minimDataList = [i for i in minimData.flat if i != 0]
        maximDataList = [i for i in maximData.flat if i != 0]
        if common.DEBUG:
            print("Length of pop:{}\n\tof dist:{}\n\tof distList:{}\n\tof roadData:{}\n\tof roadDataList:{}".format(len(pop), len(dist), len(distList), len(roadData), len(roadDataList)))


        if common.contributionSplit:
            slopeSumValues, interceptSumValues, r2SumValues , gravitySumEstimate= gravitySumContrib(pop, keys, np.array(dist), np.array(roadData), retExample=True)
            slopeValues, interceptValues, r2Values, gravityEstimate = gravity(pop, keys, dist, distList, np.array(roadDataList), retExample=True)
            if not gravityEstimate:
                print( "Gravity Estimate has no values")
                return
            if not gravitySumEstimate:
                print( "Gravity Sum Estimate has no values")
                return

            # From Gravity
            common.plotBoth(roadDataList,
                r2Values,
                slopeValues,
                interceptValues,
                r2SumValues,
                slopeSumValues,
                interceptSumValues,
                name=filename,
                titleString = titleString,
                rowExampleGravity=gravityEstimate,
                rowExampleSumGravity=gravitySumEstimate,
                useRange=True,
                rangeData=(minimDataList, maximDataList))

        else:
            slopeSumValues, interceptSumValues, r2SumValues , otherSumValues, secondOtherSumValues, gravitySumEstimate= gravitySum(pop, keys, np.array(dist), np.array(roadData), retExample=True)
            slopeValues, interceptValues, r2Values, otherValues, secondOtherValues, gravityEstimate = gravity(pop, keys, dist, distList, np.array(roadDataList), retExample=True)
            if not gravityEstimate:
                print( "Gravity Estimate has no values")
                return
            if not gravitySumEstimate:
                print( "Gravity Sum Estimate has no values")
                return

            common.plotBoth(roadDataList,
                            r2Values,
                            otherValues,
                            secondOtherValues,
                            slopeValues,
                            interceptValues,
                            r2SumValues,
                            otherSumValues,
                            secondOtherSumValues,
                            slopeSumValues,
                            interceptSumValues,
                            name=filename,
                            titleString = titleString,
                            rowExampleGravity=gravityEstimate,
                            rowExampleSumGravity=gravitySumEstimate,
                            useRange=True,
                            rangeData=(minimDataList, maximDataList))
    else:
        roadData = parseData.parseEdges(roadFile , keys)
        roadDataList = [i for i in roadData.flat if i != 0]
        if common.DEBUG:
            print("Length of pop:{}\n\tof dist:{}\n\tof distList:{}\n\tof roadData:{}\n\tof roadDataList:{}".format(len(pop), len(dist), len(distList), len(roadData), len(roadDataList)))
        slopeValues, interceptValues, r2Values, otherValues, secondOtherValues, gravityEstimate = gravity(pop, keys, dist, distList, np.array(roadDataList), retExample=True)
        if common.contributionSplit:
            slopeSumValues, interceptSumValues, r2SumValues , otherSumValues, secondOtherSumValues, gravitySumEstimate= gravitySumContrib(pop, keys, np.array(dist), np.array(roadData), retExample=True)
            if not gravityEstimate:
                print( "Gravity Estimate has no values")
                return
            if not gravitySumEstimate:
                print( "Gravity Sum Estimate has no values")
                return

            common.plotBoth(roadDataList, r2Values, otherValues, secondOtherValues, slopeValues, interceptValues, r2SumValues, otherSumValues, secondOtherSumValues, slopeSumValues, interceptSumValues, name=filename, titleString = titleString, rowExampleGravity=gravityEstimate, rowExampleSumGravity=gravitySumEstimate)

        else:

            slopeSumValues, interceptSumValues, r2SumValues , otherSumValues, secondOtherSumValues, gravitySumEstimate= gravitySum(pop, keys, np.array(dist), np.array(roadData), retExample=True)
            if not gravityEstimate:
                print( "Gravity Estimate has no values")
                return
            if not gravitySumEstimate:
                print( "Gravity Sum Estimate has no values")
                return

            # From Gravity
            common.plotBoth(roadDataList, r2Values, otherValues, secondOtherValues, slopeValues, interceptValues, r2SumValues, otherSumValues, secondOtherSumValues, slopeSumValues, interceptSumValues, name=filename, titleString = titleString, rowExampleGravity=gravityEstimate, rowExampleSumGravity=gravitySumEstimate)

if __name__=="__main__":
    # From GravitySum
    #gravityBoth(sys.argv[1], sys.argv[2], sys.argv[3])
    gravityBoth(sys.argv[1], sys.argv[2], sys.argv[3])
