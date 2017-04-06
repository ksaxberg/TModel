from airportsComplete import airports
from RoutesToCombine import combine
from RoutesToCombine import routeList
import pprint
"""
This uses the list of completed/ population listed airports
and looks through the T100 dataset, recovering a subset where
both destination and origin are airports of interest.

This program also expects an additional file, of airports to consider as the 
same. This establishes airport routes that otherwise would not be in the graph.
"""

def correctRoute(city1):
    wasMajorCity = False
    if city1 not in routeList:
        wasMajorCity = True
        return city1, wasMajorCity
    for key, collapsed in combine.items():
        if city1 in key:
            if city1 == collapsed:
                wasMajorCity = True
            city1 = collapsed
            break
    return city1, wasMajorCity

# Prints output dictionary of flight summary
# Dictionary key: origin
#  Origin dict key: dest
#    Dest dict value: [summed total passengers, distance, num flights]
flightSummary = {}
with open("../T100/T100_2015_All.csv") as f:
    f.readline()
    for line in f:
        l = line.split(',')
        passengers = float(l[0])
        distance = float(l[1])
        origin = l[3]
        # Remove quotations around airport
        origin = origin[1:-1]
        origin, origWasMajor = correctRoute(origin)
        dest = l[4]
        dest = dest[1:-1]
        dest, destWasMajor = correctRoute(dest)
        if origin > dest:
            origin, dest = dest, origin
        if origin not in airports or dest not in airports:
            continue
        if origin not in flightSummary:
            flightSummary[origin] = {}
        if dest not in flightSummary[origin]:
            if (not origWasMajor or not destWasMajor):
                flightSummary[origin][dest] = [passengers, "REPLACE", 1]
            else:
                flightSummary[origin][dest] = [passengers, distance, 1]
        else:
            flightSummary[origin][dest][0] += passengers
            flightSummary[origin][dest][2] += 1
            if origWasMajor and destWasMajor:
                flightSummary[origin][dest][1] = distance
#pprint.pprint(flightSummary)    
printPassengers = True
distance = open("distanceEdgeGrouped.txt", "w")
measured = open("measuredDataEdgeGrouped.txt", "w")
for origin, val in flightSummary.items():
    for dest, nums in val.items():
        if origin != dest and nums[0] > 0:
            # More than 0 passengers, origin is not destination
            distance.write("{0}, {1}, {2}\n".format(origin, dest, nums[1]))
            measured.write("{0}, {1}, {2}\n".format(origin, dest, nums[0]))

distance.close()
measured.close()
