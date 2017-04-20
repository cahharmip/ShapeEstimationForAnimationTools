def calulateNormals(line):
	nsl = 0
	nsr = 0
	nel = 0
	ner = 0
	return nsl,nsr,nel,ner

def calLineEquation(b0,b1,leftMostPoint,rightMostPoint):
	yInit = b0 + b1*leftMostPoint
	yDes = b0 + b1*rightMostPoint
	firstPoint = (leftMostPoint,int(yInit))
	secondPoint = (rightMostPoint,int(yDes))
	cv2.line(imgTest,secondPoint,firstPoint,(255,255,0),0)

def nextPointFromLine(line,newX):
	yDes = line[0] + line[1]*newX
	newPoint = (newX,int(yDes))
	return newPoint

class LineVertex(object):
	def __init__(self,line,lineEndPoint): # line == {(b0,b1) : vertices.sorted } // lineEndPoint == {(b0,b1) : (leftMostPoint ,rightMostPoint)}
		self.line = line
		self.start = lineEndPoint[line][0] # (xleftMost,yleftMost)
		self.end = lineEndPoint[line][1] # (xrightMost,yrightMost)
		# print "______________"
		self.normalStartL ,self.normalStartR ,self.normalEndL ,self.normalEndR = calulateNormals(line)
		self.tangentStart = None
		self.tangentEnd = None
		self.length = None # vertex that draw
		self.searchLineLenght = 0

	def growSearchLine(self):
		self.searchLineLenght += 1 # searchline 
		if self.tangentStart == None :
			self.tangentStart = [self.start,self.start]
		if self.tangentEnd == None :
			self.tangentEnd = [self.end,self.end]
		self.tangentStart[0] = nextPointFromLine(self.line, self.start[0] - self.searchLineLenght)
		self.tangentEnd[1] = nextPointFromLine(self.line, self.end[0] + self.searchLineLenght)
		print "Start : " , self.start
		print "End : " , self.end
		print "tangentStart",self.tangentStart[0]
		print "tangentEnd",self.tangentEnd[1]
		print "___________________________"
		# return "add search line."

	def checkIntersect(self):

		return "Return search line that intersect and its pair."

	def makeEdge(self, graph, neigbour):
		edge = (self.vertex,neigbour)
		graph.addEdge(edge)
