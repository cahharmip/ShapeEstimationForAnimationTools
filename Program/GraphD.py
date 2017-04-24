import cv2
import math
import numpy as np

def makeArray(vertexList):
	xArray = []
	yArray = []
	for point in vertexList:
		xArray.append(point[0])
		yArray.append(point[1])
	return xArray, yArray

def GroupToOldLine(vertex,line,verticesList,newline,kStepList):
	#checkSSE with vertex and line that intersect points on --> accept E <= 2 * Avg(R)
	rOldLine = 0.0
	rOldLineAvg = 0.0
	rNewLine = 0.0
	rNewLineAvg = 0.0
	xArrayKs,yArrayKs = makeArray(kStepList)
	verticesList.append(vertex)
	xArrayOld,yArrayOld = makeArray(verticesList)
	rOldLine,rOldLineAvg = calRSquare(line[0],line[1],xArrayOld,yArrayOld)
	# print "R Old : " ,rOldLine,rOldLineAvg
	rNewLine,rNewLineAvg = calRSquare(newline[0],newline[1],xArrayKs,yArrayKs)
	# print "R New : " ,rNewLine,rNewLineAvg
	if rOldLine <= rNewLine + 85:
		# print "BAsJung______________________________"
		return True
	else:
		return False
	# return True if rOldLineAvg*300 < rNewLineAvg else False

def calRSquare(b0,b1,xArray,yArray):
	mostDeviation = 0
	index = 0
	r = 0.0
	rAvg = 0.0
	for i in range(len(xArray)):
		r += abs(yArray[i] - (b0 + b1*xArray[i]))/math.sqrt(1+math.pow(b1,2))
		# print yApprox , yArray[i]
		if mostDeviation < r:
			mostDeviation = r
			index = i
			# print mostDeviation
	rAvg = r/len(xArray)
	xArraySorted = np.sort(xArray)
	return r,rAvg

def makeLine(kStepList):
	xArray,yArray = makeArray(kStepList)
	return LSFNormalOffset(xArray,yArray)
	# return LSFWithPerpendicularOffset(xArray,yArray)

def LSFNormalOffset(xArray,yArray):
	sumX = sum(xArray)
	sumY = sum(yArray)
	sumXY = float(0)
	sumX2 = float(0)
	sumY2 = float(0)
	b0 = float(0)
	b1 = float(0)
	size = len(xArray)
	for i in range(size):
		sumXY += xArray[i] * yArray[i]
		sumX2 += xArray[i] * xArray[i]
		sumY2 += yArray[i] * yArray[i]
	# print type(float(sumX)*float(sumX))
	try:
		b0 = (float(sumY)*sumX2-float(sumX)*sumXY)/(float(size)*sumX2-float(sumX)*sumX)
	except:
		b0 = 0.0000001
	try:	
		b1 = (float(size)*sumXY-float(sumX)*sumY)/(float(size)*sumX2-float(sumX)*sumX)
	except:
		# print "Except"
		b1 = 0.0000001
		# print b1
	return (b0,b1)

def LSFWithPerpendicularOffset(xArray,yArray):
	#y = b0 + b1x with di = abs(yi - (b0+b1(xi)))/math.sqrt(1 + b1^2)
	sumX = float(sum(xArray))
	sumY = float(sum(yArray))
	sumXY = 0.0
	sumX2 = 0.0
	sumY2 = 0.0
	b0 = 0
	b1 = 0
	n = len(xArray)
	for i in range(n):
		sumXY += xArray[i] * yArray[i]
		sumX2 += xArray[i] * xArray[i]
		sumY2 += yArray[i] * yArray[i]
	B_upleftEq = sumY2 - math.pow(sumY,2)/n
	if B_upleftEq == 0:
		B_upleftEq = 0.0001
	B_uprightEq = sumX2 - math.pow(sumX,2)/n
	if B_uprightEq == 0:
		B_uprightEq = 0.0001
	B_botEq = ((sumX*sumY)/n) - sumXY
	if B_botEq == 0:
		B_botEq = 0.0001
	B = 0.5*(B_upleftEq - B_uprightEq)/B_botEq
	print "____________________"
	print xArray
	print yArray
	print "N : ", n
	print "sumX : " , sumX , "sumY : " , sumY
	print "sumXY : ", sumXY , "sumX2 : " , sumX2 , "sumY2 : " , sumY2
	print "B_upleftEq : " , B_upleftEq
	print "B_uprightEq : " , B_uprightEq
	print "B_botEq : " , B_botEq
	print "____________________"
	if B < 0:
		b1 = -B + math.sqrt(math.pow(B,2)+1)
	else:
		b1 = -B - math.sqrt(math.pow(B,2)+1)
	b0 = (sumY - sumX*b1)/n
	return (b0,b1)

class Graph(object):
	def __init__(self, graphDict = None):
		if graphDict == None:
			graphDict = {}
		self.__graphDict = graphDict
		self.__vertexOnLineDict = {}
		self.__edgeList = None

	def getVertices(self):
		return list(self.__graphDict.keys())

	def getEdgesList(self):
		edges = []
		for vertex in self.__graphDict.keys():
			for adjacent in self.__graphDict[vertex]:
				if {vertex, adjacent} not in edges:
					edges.append((vertex,adjacent))
		return edges

	def getAdjacentsList(self,vertex):
		adjacentSet = []
		for adjacent in self.__graphDict[vertex]:
			adjacentSet.append(adjacent)
		return adjacentSet

	def getNodeWithDegreeOne(self):
		oneDegNode = []
		for node in self.__graphDict.keys():
			if len(self.__graphDict[node]) == 1:
				oneDegNode.append(node)
		# print oneDegNode
		return oneDegNode

	def getMostDegree(self):
		mostDegNode = []
		lenMax = 0
		for node in self.__graphDict.keys():
			if len(self.__graphDict[node]) > lenMax:
				lenMax = len(self.__graphDict[node])
		return lenMax

	def hasVertex(self,vertex):
		if vertex not in self.__graphDict:
			return True
		else :
			return False

	def addVertex(self,vertex):
		if vertex not in self.__graphDict:
			self.__graphDict[vertex] = []

	def addEdge(self,edge):
		#edge is in list form.
		edge = set(edge)
		(vertex1, vertex2) = tuple(edge)
		if vertex1 in self.__graphDict:
			if vertex2 not in set(self.__graphDict[vertex1]):
				self.__graphDict[vertex1].append(vertex2)
		else:
			self.__graphDict[vertex1] = [vertex2]
		if vertex1 not in set(self.__graphDict[vertex2]):
			self.__graphDict[vertex2].append(vertex1)

	def checkLength(self):
		return len(self.__graphDict) 

	def subGraphToLineBFS(self,imgTest):
		leastX = 9999
		leftMost = 9999
		stack = []
		for vertex in self.__graphDict:
			# print vertex
			if vertex[0] < leastX:
				leastX = vertex[0]
				leftMost = vertex
		# print leftMost
		stack.append(leftMost)
		lineDict = {} # [line] : [(vertex1,vertex2),...]
		vertexOnLineDict = {} # [vertex] : (b0,b1)
		kStepList = []
		kStepList.append(leftMost)
		newline = None
		visited = set()
		visited.add(leftMost)
		mostDeg = self.getMostDegree() + 30
		removed = 0
		while(stack):
			visit = stack.pop()
			# print visit
			addedVertex = False
			for vertex in self.getAdjacentsList(visit):
				if vertex not in visited:
					visited.add(vertex)
					stack.append(vertex)
					kStepList.append(vertex)
					addedVertex = True
			if len(kStepList) >= mostDeg :
				dellist = kStepList[:]
				newline = makeLine(kStepList)
				if lineDict:
					for vertex in kStepList:
						for adjacent in self.getAdjacentsList(vertex):
							if adjacent in vertexOnLineDict:
								if GroupToOldLine(vertex,vertexOnLineDict[adjacent],lineDict[vertexOnLineDict[adjacent]],newline,kStepList): # True : select old-line
									lineDict[vertexOnLineDict[adjacent]].append(vertex)
									lineAdded = makeLine(lineDict[vertexOnLineDict[adjacent]])
									lineDict[lineAdded] = lineDict.pop(vertexOnLineDict[adjacent])
									for vertexAdded in lineDict[lineAdded]:
										vertexOnLineDict[vertexAdded] = lineAdded	
									dellist.remove(vertex)
									newline = makeLine(dellist)
									# print "VERTEX ADDED TO OLDLINE!!"
									removed = 1
									break
				kStepList = dellist[:]
			elif addedVertex == False:
				dellist = kStepList[:]
				newline = makeLine(kStepList)
				if lineDict:
					for vertex in kStepList:
						for adjacent in self.getAdjacentsList(vertex):
							if adjacent in vertexOnLineDict:
								if GroupToOldLine(vertex,vertexOnLineDict[adjacent],lineDict[vertexOnLineDict[adjacent]],newline,kStepList): # True : select old-line
									lineDict[vertexOnLineDict[adjacent]].append(vertex)
									lineAdded = makeLine(lineDict[vertexOnLineDict[adjacent]])
									lineDict[lineAdded] = lineDict.pop(vertexOnLineDict[adjacent])
									for vertexAdded in lineDict[lineAdded]:
										vertexOnLineDict[vertexAdded] = lineAdded	
									dellist.remove(vertex)
									newline = makeLine(dellist)
									# print "VERTEX ADDED TO OLDLINE!!"
									removed = 1
									break
				kStepList = dellist[:]
				if len(kStepList) != 0:
					# print "Make line1 !!!!"
					newline = makeLine(kStepList)
					lineDict[newline] = kStepList
					for vertex in kStepList:
						vertexOnLineDict[vertex] = newline
					kStepList = []
			if len(kStepList) >= mostDeg:
				newline = makeLine(kStepList)
				lineDict[newline] = kStepList
				for vertex in kStepList:
					vertexOnLineDict[vertex] = newline
				kStepList = []

		# print len(lineDict.keys())
		return lineDict,vertexOnLineDict

	def printGraph(self,imgTest):
		res = ""
		for vertex in self.__graphDict.keys():
			for adj in self.__graphDict[vertex]:
				cv2.line(imgTest,(vertex),(adj),(255,0,125),0)
		# print res

