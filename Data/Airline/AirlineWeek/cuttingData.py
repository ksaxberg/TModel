from __future__ import print_function
import sys
import pprint
import airplaneKeys
# Get list of selected airports
ports = ["AXA","AUA","DOM","VIJ","EIS","SXM","SBH","SFG","FDF","PTP","CAY"]

with open(sys.argv[1], 'r') as f:
	for line in f:
		l = line.strip().split(',')
		port1, port2, date, airplane, time = [x.strip() for x in l]
		if port1 in ports and port2 in ports:
			print("{}, {}, {}".format(port1, port2, 
				str(airplaneKeys.airplaneKeys[airplane])))
	#print("Airports of interest: {}".format(str(ports)))
#airplanes = []
#with open(sys.argv[1], 'r') as f:
#	for line in f:
#		l = line.strip().split(',')
#		s = l[3].strip()
#		if s not in airplanes:
#			airplanes.append(s)
#	print("Airplanes of interest: {}".format(str(airplanes)))
#d = {}
#with open(sys.argv[1], 'r') as f:
#	for line in f:
#		l = line.strip().split(',')
#		s = l[1].strip()
#		if s in ports:
#			#Have destination airport of interest	
#			key = (l[0].strip(), s)
#			if key in d:
#				#Replace 1 with plane type translation
#				d[key] += 1
#			else:
#				d[key] = 1
#	#print("Collapsed route representation: \n{}".format(pprint.pformat(d)))
#	for key, val in d.items():
#		print("{}, {}, {}".format(key[0], key[1], val))
