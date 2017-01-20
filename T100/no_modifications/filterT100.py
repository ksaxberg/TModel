from airportsComplete import airports
import pprint


# Prints output dictionary of flight summary
# Dictionary key: origin
#  Origin dict key: dest
#    Dest dict value: [summed total passengers, distance, num flights]
flightSummary = {}
with open("T100_2015_All.csv") as f:
    f.readline()
    for line in f:
        l = line.split(',')
        passengers = float(l[0])
        distance = float(l[1])
        origin = l[3]
        # Remove quotations around airport
        origin = origin[1:-1]
        dest = l[4]
        dest = dest[1:-1]
        if origin not in airports or dest not in airports:
            continue
        if origin not in flightSummary:
            flightSummary[origin] = {}
        if dest not in flightSummary[origin]:
            flightSummary[origin][dest] = [passengers, distance, 1]
        else:
            flightSummary[origin][dest][0] += passengers
            flightSummary[origin][dest][2] += 1
#pprint.pprint(flightSummary)    
printPassengers = True
distance = open("distanceEdge.txt", "w")
measured = open("measuredDataEdge.txt", "w")
for origin, val in flightSummary.items():
    for dest, nums in val.items():
        if origin != dest and nums[0] > 0:
            # More than 0 passengers, origin is not destination
            distance.write("{0}, {1}, {2}\n".format(origin, dest, nums[1]))
            measured.write("{0}, {1}, {2}\n".format(origin, dest, nums[0]))

distance.close()
measured.close()
