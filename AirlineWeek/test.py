from __future__ import print_function
import sys
import pprint

# Get list of selected airports
ports = []
with open(sys.argv[1], 'r') as f:
	for line in f:
		l = line.strip().split(',')
		s = l[0].strip()
		if s not in ports:
			ports.append(s)
	#print("Airpots of interest: {}".format(str(ports)))

d = {}
with open(sys.argv[1], 'r') as f:
	for line in f:
		l = line.strip().split(',')
		s = l[1].strip()
		if s in ports:
			#Have destination airport of interest	
			key = (l[0].strip(), s)
			if key in d:
				#Replace 1 with plane type translation
				d[key] += 1
			else:
				d[key] = 1
	#print("Collapsed route representation: \n{}".format(pprint.pformat(d)))
	for key, val in d.items():
		print("{}, {}, {}".format(key[0], key[1], val))
