import parseData
from RoutesToCombine import combine

"""
Reduces the distance length of the route by 1
Also filters edges that have distance less than threshold

Format to call:
python RouteDistanceModify.py
 -- requires correct files to be in current directory
"""

DistanceThreshold = 0
RouteChange = "RoutesThatNeedChanging.txt"
Routes = "distanceEdgeUnchanged.txt"
MeasuredData = "measuredDataEdgeUnchanged.txt"
pop = "population.txt"
keys = parseData.makeKeys(pop)
Change = {}

def collapseRoutes(city1, city2):
    for key, collapsed in combine.items():
        if city1 in key:
            city1 = collapsed
            break
    for key, collapsed in combine.items():
        if city2 in key:
            city2 = collapsed
            break
    return city1, city2


with open(RouteChange) as f:
    #City1, City2 here are integers
    for line in f:
        city1, city2, oldDist = [x.strip() for x in line.strip().split(',')]
        city1 = int(city1)
        city2 = int(city2)
        oldDIst = float(oldDist)
        if city1 not in keys.keys() or city2 not in keys.keys():
            raise ValueError("City \"{}\" or City \"{}\" isn't in the key".format(city1, city2))
        if city1 > city2:
            city1, city2 = city2, city1
        #City 1 is smaller index
        if keys[city1] in Change.keys():
            Change[keys[city1]] += [keys[city2]]
        else:
            Change[keys[city1]] = [keys[city2]]
previousDistances = {}
with open(Routes) as f:
    # city1 and city2 here are city names
    for line in f:
        city1, city2, oldDist = [x.strip() for x in line.strip().split(',')]
        oldDist = float(oldDist)
        city1, city2 = collapseRoutes(city1, city2)
        if(city1 == city2):
            continue
        #City 1 is smaller index
        if city1 in previousDistances.keys():
            if city2 in previousDistances[city1].keys():
                #Shouldnt be here
                #print("You're in an error zoooone")
                unUsedVariable = 0
            else:
                if city1 in Change.keys() and city2 in Change[city1]:
                    previousDistances[city1][city2] = [oldDist -1]
                else:
                    previousDistances[city1][city2] = [oldDist]
                    
        else:
            if city1 in Change.keys() and city2 in Change[city1]:
                previousDistances[city1]= {city2: [oldDist -1]}
            else:
                previousDistances[city1] = {city2: [oldDist]}
with open(MeasuredData) as f:
    for line in f:
        city1, city2, data = [x.strip() for x in line.strip().split(',')]
        data = float(data)
        city1, city2 = collapseRoutes(city1, city2)
        if(city1 == city2):
            continue
        if city1 in previousDistances.keys():
            if len(previousDistances[city1][city2]) == 2:
                previousDistances[city1][city2][1] += data
            else: 
                previousDistances[city1][city2] += [data]

distFile = open("distanceEdgeEdited.txt", "w")
dataFile = open("measuredDataEdgeEdited.txt", "w")
for origin, val in previousDistances.items():
    for dest, num in val.items():
        if origin != dest and len(num) == 2 and num[0] > 0:
            # More than 0 passengers, origin is not destination
            if num[0] > DistanceThreshold: 
                #Also adding in distanceThreshold here
                distFile.write("{0}, {1}, {2}\n".format(origin, dest, str(num[0])))
                dataFile.write("{0}, {1}, {2}\n".format(origin, dest, str(num[1])))
distFile.close()
dataFile.close()

