class LineVertex(object):
	def __init__(self,line,lineEndPoint): # line == {(b0,b1) : vertices.sorted } // lineEndPoint == {(b0,b1) : (leftMostPoint ,rightMostPoint)}
		self.start = lineEndPoint[line][0]
		self.end = lineEndPoint[line][1]
		self.normalStart = None
		self.normalEnd = None
		self.tangentStart = None
		self.tangentEnd = None
		self.length = None # vertex that draw

	def growSearchLine(self):
		return "add search line."

	def checkIntersect(self):
		return "Return search line that intersect and its pair."

	def makeEdge(self, graph, neigbour):
		edge = (self.vertex,neigbour)
		graph.addEdge(edge)
