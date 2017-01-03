import sys
import pprint

airports = {} 
with open(sys.argv[1], 'r') as f:
    f.readline()
    for line in f:
        passengers = float(line.split(',')[0])
        service = line.split(',')[-2]
        if service != '"F"' and service != '"L"':
            continue 
        first = line.split(',')[3]
        first = first[1:-1]
        second = line.split(',')[4]
        second = second[1:-1]
        if first not in airports.keys():
            airports[first] = [0, 0, 0]
        if second not in airports.keys():
            airports[second] = [0, 0, 0]
        airports[first][0] += 1
        airports[first][1] += passengers
        airports[second][0] += 1
        airports[second][2] += passengers

ports = airports.items()
ports.sort(key=lambda x: x[1])
pprint.pprint(ports[::-1])
