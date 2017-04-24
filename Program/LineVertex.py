import math

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

def normalizeVector(directionVector):
	mag = math.sqrt(directionVector[0]*directionVector[0] + directionVector[1]*directionVector[1])
	if mag == 0:
		return (0,0)
	normx = directionVector[0]/mag
	normy = directionVector[1]/mag
	temp = normx
	normx = -normy
	normy = temp
	norm = (normx , normy)
	return norm

def directionVector(directionVector):
	mag = math.sqrt(directionVector[0]*directionVector[0] + directionVector[1]*directionVector[1])
	if mag == 0:
		return (0,0)
	normx = directionVector[0]/mag
	normy = directionVector[1]/mag
	norm = (normx , normy)
	return norm

class LineVertex(object):
	def __init__(self,line,lineEndPoint): # line == {(b0,b1) : vertices.sorted } // lineEndPoint == {(b0,b1) : (leftMostPoint ,rightMostPoint)}
		self.line = line
		# print line.keys()[0]
		# self.linePerp = calulateNormals(line,lineEndPoint[line]) #linePerp == (linePerpStart,linePerpEnd)
		self.start = lineEndPoint[line.keys()[0]][0] # (xlMost,ylMost)
		# print self.start
		self.end = lineEndPoint[line.keys()[0]][1] # (xrMost,yrMost)
		# print math.pow(self.start[0]-self.end[0],2) - math.pow(self.start[1]-self.end[1],2)
		self.lineSize = math.sqrt(math.pow(self.start[0]-self.end[0],2) + math.pow(self.start[1]-self.end[1],2))
		self.directionVector = (self.end[0] - self.start[0], self.end[1] - self.start[1])
		self.norm = normalizeVector(self.directionVector)
		self.normtan = directionVector(self.directionVector)
		self.normalStartL = (self.norm, [self.start,self.start]) 
		self.normalStartR = (self.norm, [self.start,self.start])
		self.normalEndL = (self.norm, [self.end,self.end])
		self.normalEndR = (self.norm, [self.end,self.end])
		self.tangentStart = (self.normtan,[self.start,self.start])
		self.tangentEnd = (self.normtan,[self.end,self.end])
		self.length = [self.start,self.end] # vertex that draw	
		self.searchLineLength = 0

	def getLineSize(self):
		return self.lineSize

	def degradeSearchLineLength(self):
		if self.searchLineLength > 10:
			self.searchLineLength -= int(self.searchLineLength*2/3)
		else:
			self.searchLineLength -= int(self.searchLineLength/2)

	def growSearchLine(self):
		self.searchLineLength += 1 # searchline 
		self.growTangent(self.searchLineLength)
		self.growNormals(self.searchLineLength)
		# return "add search line."

	def getVertexData(self):
		lineData = self.line
		tangent = (self.tangentStart, self.tangentEnd) # ([spoint,origin],[origin,spoint])
		normals = (self.normalStartL, self.normalStartR, self.normalEndL, self.normalEndR) #([spoint,origin],[origin,spoint] ...)
		length = (self.start, self.end)
		return lineData,tangent,normals,length

	def confiqRange(self,tangentStartLast,tangentEndLast,normalStartR,normalStartL,normalEndR,normalEndL):
		self.tangentStart[1] = tangentStartLast
		self.tangentEnd[0] = tangentEndLast
		self.normalStartR[1] = normalStartR
		self.normalStartL[0] = normalStartL
		self.normalEndR[1] = normalEndR
		self.normalEndL[0] = normalEndL
		return 0

	def growTangent(self,length):
		self.tangentStart[1][0] = (int(self.start[0] + self.tangentStart[0][0] * (-length)), int(self.start[1]  + self.tangentStart[0][1] * -length))
		self.tangentEnd[1][0] = (int(self.end[0] + self.tangentEnd[0][0] * (length)), int(self.end[1]  + self.tangentEnd[0][1] * (length)))

	def growNormals(self,length):
		# print "NormalStartL",self.normalStartL[0][0]
		self.normalStartL[1][0] = (int(self.start[0] + self.normalStartL[0][0] * length), int(self.start[1]  + self.normalStartL[0][1] * length))
		self.normalStartR[1][0] = (int(self.start[0] + self.normalStartR[0][0] * (-length)), int(self.start[1]  + self.normalStartR[0][1] * -(length)))
		self.normalEndL[1][0] = (int(self.end[0] + self.normalEndL[0][0] * length), int(self.end[1]  + self.normalEndL[0][1] * length))
		self.normalEndR[1][0] = (int(self.end[0] + self.normalEndR[0][0] * (-length)), int(self.end[1]  + self.normalEndR[0][1] * -(length)))