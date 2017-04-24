import cv2
import math
import random
import bisect
import networkx as nx
from TestNx import TestNx
from TesTree import Tree
from GraphD import Graph
from LineGraph import LineGraph
from LineVertex import LineVertex
import numpy as np
import subprocess
import scipy.optimize as optimization
from matplotlib import pyplot

#-------- Global Var --------
imgTest = 0
#----------------------------

#----------------------- Prepare Data ---------------------------------

def getFileName():
	ls_output = subprocess.check_output('ls',cwd='Test_picture')
	ls_output_list = ls_output.split('\n')
	ls_output_list.remove('')
	return ls_output_list

def auto_canny(image, sigma=0.33):
	v = np.median(image)
	lower = int(max(0,(1.0-sigma)*v))
	upper = int(min(255,(1.0-sigma)*v))
	edged = cv2.Canny(image,lower,upper)
	return edged

def drawApproxLine(b0,b1,leftMostPoint,rightMostPoint,lineEndPointDict,line):
	yInit = b0 + b1*leftMostPoint
	yDes = b0 + b1*rightMostPoint
	# print "_____ Check left&right Point ______"
	firstPoint = (leftMostPoint,int(yInit))
	secondPoint = (rightMostPoint,int(yDes))
	lineEndPointDict[line] = (firstPoint,secondPoint)
	# cv2.line(imgTest,secondPoint,firstPoint,(255,255,0),0)

def drawApproxLineX(b0,b1,leftMostPoint,rightMostPoint,color,imgTmp):
	yInit = b0 + b1*leftMostPoint
	yDes = b0 + b1*rightMostPoint
	print "_____ Drawing a line ______"
	firstPoint = (leftMostPoint,int(yInit))
	secondPoint = (rightMostPoint,int(yDes))
	# print firstPoint ,secondPoint
	cv2.line(imgTmp,secondPoint,firstPoint,color,0)

def myDrawContour(contour):
	a,b,c = random.randint(0,255),random.randint(0,255),random.randint(0,255)
	for i in range(len(contour)):
		if i != len(contour) - 1:
			cv2.line(imgTest,(contour[i][0][0],contour[i][0][1]),(contour[i+1][0][0],contour[i+1][0][1]),(a,b,c),0)

def groupListToTree(treeSet, listOfContoursList):
	x = 0
	for i in range (len(listOfContoursList)):
		treeSet.append(Tree(listOfContoursList[i]))

def contoursToGraphList(contours):
	graphList = []
	for contour in contours:
		if len(contour) > 4:
			tmpGraph = Graph()
			#add vertex
			for point in contour:
				tmpGraph.addVertex((point[0][0],point[0][1]))

			#add edge
			for index in range(len(contour) - 1):
				tmpGraph.addEdge([(contour[index][0][0],contour[index][0][1]), (contour[index+1][0][0],contour[index+1][0][1])])

			graphList.append(tmpGraph)
	return graphList

def lineToLineVertexAndLineGraph(lineDict,lineEndPointDict,lineGraph):
	for line in lineDict:
		tmpLineVertex = LineVertex({line:lineDict[line]},lineEndPointDict)
		lineGraph.addVertex(tmpLineVertex)
	return lineGraph

def getLongestLenghtGraph(graphList):
	longestList = 0
	longestIndex = 0
	for index in range(len(graphList)):
		if graphList[index].checkLength() > longestList:
			longestList = graphList[index].checkLength()
			longestIndex = index
	return graphList[longestIndex]	

def makeLineDictWithEndPoints(lineDict):
	lineEndPointDict = {}
	for line in lineDict:
			leftMostPoint = (99999,0)
			rightMostPoint = (0,0)
			# a,b,c = random.randint(50,255),random.randint(50,255),random.randint(50,255)
			for vertex in lineDict[line]:
				# imgTest[vertex[1]][vertex[0]] = (a,b,c)
				if vertex[0] < leftMostPoint[0]: 
					leftMostPoint = vertex
				if vertex[0] > rightMostPoint[0]:
					rightMostPoint = vertex	
			drawApproxLine(line[0],line[1],leftMostPoint[0],rightMostPoint[0],lineEndPointDict,line)
	return lineEndPointDict
#-----------------------------------------------------------------------

#--------------------------- Calculation -------------------------------
def BresenhamLine(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def checkIntersectTangent(bresenhamIndex,tangentPoint,line,height,width,graph):
	# print tangentPoint
	for point in tangentPoint:
		if point[1] >= height:
			imgTest[height-1][point[0]] = (255,0,0)
		elif point[0] >= width:
			imgTest[point[1]][width-1] = (255,0,0)
		else:
			imgTest[point[1]][point[0]] = (255,0,0)
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			if intersectType == "tangent"and intersectLine != line:
				# print "addEdgeWithType L-Junction"
				graph.addEdge(line,intersectLine,"L-Junction")
			elif intersectType == "normals"and intersectLine != line:
				# print "addEdgeWithType Collinearity"
				graph.addEdge(line,intersectLine,"Colinearity")
			else:
				# print "addEdgeWithType T-Junction"
				i = 0
				# graph.addEdge(line,intersectLine,"T-Junction")
		else:
			bresenhamIndex[point] = (line,"tangent")

def checkIntersectNormals(bresenhamIndex,normalsPoint,line,height,width,graph):
	for point in normalsPoint:
		if point[1] >= height:
			imgTest[height-1][point[0]] = (140,255,100)
		elif point[0] >= width:
			imgTest[point[1]][width-1] = (140,255,100)
		else :
			imgTest[point[1]][point[0]] = (140,255,100)
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			if intersectType == "tangent"and intersectLine != line:
				# print "addEdgeWithType Collinearity"
				graph.addEdge(line,intersectLine,"Colinearity")
		else:
			bresenhamIndex[point] = (line,"normals")

def checkIntersectLine(bresenhamIndex,lenghtPoint,line,graph):
	for point in lenghtPoint:
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			# if intersectType == "tangent" and intersectLine != line:
			# 	graph.addEdge(line,intersectLine,"L-Junction")
				# print "addEdgeWithType T-junction"
				# graph.addEdge(line,intersectLine,"T-Junction")
		else:
			bresenhamIndex[point] = (line,"normals")

def drawAndCheckIntersectInBresenhamIndex(bresenhamIndex,line,tangent,normals,lenght,height,width,graph):
	tangentStartPoint = BresenhamLine(tangent[0][1][1],tangent[0][1][0])
	tangentEndPoint = BresenhamLine(tangent[1][1][0],tangent[1][1][1])
	normalStartRPoint = BresenhamLine(normals[0][1][0],normals[0][1][1])
	normalStartLPoint = BresenhamLine(normals[1][1][0],normals[1][1][1])
	normalEndRPoint = BresenhamLine(normals[2][1][0],normals[2][1][1])
	normalEndLPoint = BresenhamLine(normals[3][1][0],normals[3][1][1])
	lenghtPoint = BresenhamLine(lenght[0],lenght[1])

	checkIntersectTangent(bresenhamIndex,tangentStartPoint,line,height,width,graph)
	checkIntersectTangent(bresenhamIndex,tangentEndPoint,line,height,width,graph)
	checkIntersectNormals(bresenhamIndex,normalStartRPoint,line,height,width,graph)
	checkIntersectNormals(bresenhamIndex,normalStartLPoint,line,height,width,graph)
	checkIntersectNormals(bresenhamIndex,normalEndRPoint,line,height,width,graph)
	checkIntersectNormals(bresenhamIndex,normalEndLPoint,line,height,width,graph)
	checkIntersectLine(bresenhamIndex,lenghtPoint,line,graph)
	return tangentStartPoint, tangentEndPoint, normalStartRPoint, normalStartLPoint

#-----------------------------------------------------------------------

def main():
	global imgTest
	image_list = getFileName() #circleNaturalHighlight #cubeGreenUnderShadeNoon #complexSqGreenNoonLight
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/cubeGreenUnderShadeNoon.jpg'),cv2.COLOR_BGR2RGB) 
	height,width = imgRGBcube.shape[:2]
	imgTest = np.zeros((height,width,3), np.uint8)
	imgTest = imgRGBcube[:] / 4
	imgRGBcube = cv2.blur(imgRGBcube,(5,5))
	edgesRGBcube = auto_canny(imgRGBcube)
	im2, contours, hierarchy = cv2.findContours( edgesRGBcube.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	graphList = contoursToGraphList(contours)
	graphLongest = getLongestLenghtGraph(graphList)
	lineGraphAll = LineGraph()
	tnx = TestNx()
	nxGraph = nx.Graph()
	for graph in graphList:
		lineDict , vertexOnLineDict = graph.subGraphToLineBFS(imgTest)
		lineEndPointDict = makeLineDictWithEndPoints(lineDict)
		lineToLineVertexAndLineGraph(lineDict,lineEndPointDict,lineGraphAll)
		bresenhamIndex = {}
	countCyclic = 0
	cycleList = {}
	gg = 0
	# ---------- Ranking ------------ #
	rankList = []
	for line in lineGraphAll.getVertices():
		if gg == 0 :
			print type(line) 
		gg=1
		lineData,tangent,normals,lenght = line.getVertexData()
		rankList.append((line,line.getLineSize()))
	rankLine = sorted(rankList, key=lambda line: line[1],reverse=True)
	# print rankLine
	# print 'Sorpted'
	# -------------------------------- # 
	# print len(rankList)

	while len(cycleList) < 7:
		#-------- Make Random ---------#
		chosenLine = []
		rng = np.random.exponential(scale=1.0) 
		if rng <= 1:
			chosenLine = rankLine[:int(len(rankLine)*0.2)]
		else:
			chosenLine  = rankLine[int(len(rankLine)*0.2):]

		#------------------------------#

		for line in chosenLine:  #>>>> O(N)
			line[0].growSearchLine()
			lineData,tangent,normals,lenght = line[0].getVertexData()
			tnx.drawAndCheckIntersectInBresenhamIndexNx(bresenhamIndex,line[0],tangent,normals,lenght,height,width,nxGraph,imgTest)
			nxList = nx.cycle_basis(nxGraph)
			# for x in nxList:
			# 	for j in x:
			# 		print j
			# 		print nxGraph[j <<<< This code will get edge.
			countCyclic += len(nxList)
			# countCyclic += 1
			for node in nxList:
				nodeTuple = tuple(node)
				if len(node) > 6:
					if nodeTuple not in cycleList:
						cycleList[nodeTuple] = True
						print "Convex detected!!"
				for lineCyclic in node:
					lineCyclic.degradeSearchLineLength()


	for nodes in cycleList:
		imgTmp = np.zeros((height,width,3), np.uint8)
		print "Figure_______________________________________________"
		for x in nodes:
			print nxGraph[x]
		print "_____________________________________________________"
		# imgTmp = imgTest[:]
		color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
		for line in nodes:
			lineData,tangent,normals,lenght = line.getVertexData()
			leftMostPoint = (99999,0)
			rightMostPoint = (0,0)
			for vertex in lineData.values()[0]:
				if vertex[0] < leftMostPoint[0]: 
					leftMostPoint = vertex
				if vertex[0] > rightMostPoint[0]:
					rightMostPoint = vertex
			drawApproxLineX(lineData.keys()[0][0],lineData.keys()[0][1],leftMostPoint[0],rightMostPoint[0],color,imgTmp)

		# pyplot.imshow(imgTest)
		pyplot.figure()
		pyplot.imshow(imgTmp)
	pyplot.figure()
	pyplot.imshow(imgTest)
	pyplot.show()

	# pyplot.imshow(imgTest)

if __name__ == "__main__":
	main()