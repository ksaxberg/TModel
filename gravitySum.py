import sys
import graviy
import math

class Vertex:

	def __init__(self, distance, predecessor, name):
		self.d = distance
		self.pi = predecessor
		self.name = name
	def pi():
		return self.pi
	def d():
		return self.d
	def name(): 
		return self.name
	def changeDistance(newDistance):
		self.d = newDistance
	def relax(distance, predecessor):
		self.d = distance
		self.pi = predecessor
class MinQueue:
	"A minQueue for use in Dijkstra's Algorithm"
	def __init__(self, source, vertices):
		self.queue = {}
		#The Initialize-Single-Source
		#	Storing queue[vertex] = [distance, predecessor]
		for i in range(vertices):
			queue[i] = Vertex(math.inf, 'nil', i)
		#Setting the source node
		self.minimum = source
		queue[source] = Vertex(0, 'nil', source)
	def minimum():
		if !self.empty:
			return queue[self.minimum]
		else:
			return -1
	def extractMin():
		if !self.empty:
			temp = self.queue.pop(self.minimum)
			newMin= min(self.queue.items(), key=lambda x: x[1].d())
			self.minimum = newMin[0]
			return temp
		else:
			return -1
	def relax(elementX, distance, newSource):
		#Assuming: distance is distance from newSource to ElementX
		#  newSource is a full vertex class
		if self.queue[elementX].d() > newSource.d() + distance:
			self.queue[elementX].relax(distance+newSource.d(), newSource.name())   
		

def runDijkstra(distance, source, destination, memory):
	if([source, destination] in memory.keys() ):
		return memory[[source, destination]]
	if([destination, source] in memory.keys()):
		return memory[[destination, source]]
		
	vertices = range(len(distance))
	for i in range(len(distance)):
		if i != source:
			
	

def gravitySum(pop, distances, roadData):
	overlappingRoutes = runDijkstra(distance)
	


if __name__ == '__main__':
	import sys
	import parseData
	if(len(sys.argv)==4  ):
		pop = parseData.parsePopulation(sys.argv[1]);
		dist = parseData.parseDistance(sys.argv[2]);
		roadData = parseData.parseDistance(sys.argv[3]);
		x,y,z = formatRawMatrices(pop, dist, roadData);
		analysis = runGravity(x,y,z);
		print("[Beta, Slope, R^2, slope, intercept, R^2]")
		pprint.pprint(analysis)
