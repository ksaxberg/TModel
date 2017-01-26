import sys
filename = sys.argv[1]
"""
Takes in the list that looks like ORIGIN, DESTINATION, PASSENGERS
that contains multiples of each element, sums them together.
Currently commented out....
"""

d = {}
with open(filename) as f:
    for line in f:
        orig, dest, nums = [a.strip() for a in line.strip().split(',')]
        if (orig, dest) not in d.keys() and (dest, orig) not in d.keys():
            d[(orig, dest)] = float(nums)
        #if (orig, dest) in d.keys():
        #    #d[(orig, dest)] += float(nums)
        #elif (dest, orig) in d.keys():
        #    #d[(dest, orig)] += float(nums)
        #else:
        #    d[(orig, dest)] = float(nums)
for cities, nums in d.items():
    print("{0}, {1}, {2}".format(cities[0], cities[1], nums))
