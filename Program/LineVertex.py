def calulateNormals(line, startAndEndPoint): #<<<<< PROBLEM IS DIVIDE BY ZERO AND HOW TO ADD POINT JUST ONE IF SLOPE == 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
	sNode = startAndEndPoint[0]
	eNode = startAndEndPoint[1]
	#makePerpendicularLine
	# print "b1 : ",line[1]
	try:
		b1Perp = -1.0/line[1]               
	except:
		b1Perp = 0
	b0PerpStart = sNode[1] + b1Perp*sNode[0]
	b0PerpEnd = eNode[1] + b1Perp*eNode[0]
	linePerpStart = (b0PerpStart,b1Perp)
	linePerpEnd = (b0PerpEnd,b1Perp)
	return (linePerpStart,linePerpEnd)

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
		self.linePerp = calulateNormals(line,lineEndPoint[line]) #linePerp == (linePerpStart,linePerpEnd)
		self.start = lineEndPoint[line][0] # (xlMost,ylMost)
		self.end = lineEndPoint[line][1] # (xrMost,yrMost)
		self.normalStartL = None
		self.normalStartR = None
		self.normalEndL = None
		self.normalEndR  = None
		self.tangentStart = None
		self.tangentEnd = None
		self.length = [self.start,self.end] # vertex that draw
		self.searchLineLenght = 0

	def growSearchLine(self):
		self.searchLineLenght += 1 # searchline 
		self.growTangent(self.searchLineLenght)
		self.growNormals(self.searchLineLenght)
		# return "add search line."

	def getVertexData(self):
		tangent = (self.tangentStart, self.tangentEnd) # ([spoint,origin],[origin,spoint])
		normals = (self.normalStartL, self.normalStartR, self.normalEndL, self.normalEndR) #([spoint,origin],[origin,spoint] ...)
		length = (self.start, self.end)
		return tangent,normals,length

	def confiqRange(self,tangentStartLast,tangentEndLast,normalStartR,normalStartL,normalEndR,normalEndL):
		self.tangentStart[1] = tangentStartLast
		self.tangentEnd[0] = tangentEndLast
		self.normalStartR[1] = normalStartR
		self.normalStartL[0] = normalStartL
		self.normalEndR[1] = normalEndR
		self.normalEndL[0] = normalEndL
		return 0

	def makeEdge(self, graph, neigbour):
		edge = (self.vertex,neigbour)
		graph.addEdge(edge)

	def growTangent(self,length):
		if self.tangentStart == None :
			self.tangentStart = [self.start,self.start]
		if self.tangentEnd == None :
			self.tangentEnd = [self.end,self.end]
		self.tangentStart[0] = nextPointFromLine(self.line, self.start[0] - length)
		self.tangentEnd[1] = nextPointFromLine(self.line, self.end[0] + length)
		# print "Start : " , self.start
		# print "End : " , self.end
		# print "tangentStart",self.tangentStart[0]
		# print "tangentEnd",self.tangentEnd[1]
		# print "___________________________"

	def growNormals(self,length):
		if self.normalStartR == None and self.normalStartL == None :
			self.normalStartR = [self.start,self.start]
			self.normalStartL = [self.start,self.start]
		if self.normalEndR == None and self.normalEndL == None :
			self.normalEndR = [self.end,self.end]
			self.normalEndL = [self.end,self.end]
		self.normalStartR[0] = nextPointFromLine(self.linePerp[0],self.start[0] - length)
		self.normalStartL[1] = nextPointFromLine(self.linePerp[0],self.start[0] + length)
		self.normalEndR[0] = nextPointFromLine(self.linePerp[1],self.end[0] - length)
		self.normalEndL[1] = nextPointFromLine(self.linePerp[1],self.end[0] + length)
		print "Start : " , self.start
		print "End : " , self.end
		print "normalStartR ",self.normalStartR[0]
		print "normalStartL ",self.normalStartL[1]
		print "normalEndR ",self.normalEndR[0]
		print "normalEndL ",self.normalEndL[1]
		print "___________________________"