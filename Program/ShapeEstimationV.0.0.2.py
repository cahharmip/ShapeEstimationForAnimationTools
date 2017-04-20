import cv2
import math
import random
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
	# print "FirstPoint" , firstPoint
	# print "SecondPoint", secondPoint
	cv2.line(imgTest,secondPoint,firstPoint,(255,255,0),0)

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

def lineToLineVertexAndLineGraph(lineDict,lineEndPointDict):
	lineGraph = LineGraph()
	for line in lineDict:
		tmpLineVertex = LineVertex(line,lineEndPointDict)
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

def checkIntersectTangent(bresenhamIndex,tangentPoint,line):
	for point in tangentPoint:
		print point
		imgTest[point[1]][point[0]] = (255,0,0)
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			if intersectType == "tangent":
				print "addEdgeWithType L-Junction"
			elif intersectType == "normals":
				print "addEdgeWithType Collinearity"
			else:
				print "addEdgeWithType T-Junction"
		else:
			bresenhamIndex[point] = (line,"tangent")

def checkIntersectNormals(bresenhamIndex,normalsPoint,line):
	for point in normalsPoint:
		imgTest[point[1]][point[0]] = (140,255,140)
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			if intersectType == "tangent":
				print "addEdgeWithType Collinearity"
		else:
			bresenhamIndex[point] = (line,"normals")

def checkIntersectLine(bresenhamIndex,lenghtPoint,line):
	for point in lenghtPoint:
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			if intersectType == "tangent":
				print "addEdgeWithType T-junction"
		else:
			bresenhamIndex[point] = (line,"normals")

def drawAndCheckIntersectInBresenhamIndex(bresenhamIndex,line,tangent,normals,lenght):
	tangentStartPoint = BresenhamLine(tangent[0][0],tangent[0][1])
	# print tangentStartPoint
	tangentEndPoint = BresenhamLine(tangent[1][0],tangent[1][1])
	# print tangentEndPoint
	normalStartRPoint = BresenhamLine(normals[0][0],normals[0][1])
	# print normalStartRPoint
	normalStartLPoint = BresenhamLine(normals[1][0],normals[1][1])
	# print normalStartLPoint
	normalEndRPoint = BresenhamLine(normals[2][0],normals[2][1])
	# print normalEndRPoint
	normalEndLPoint = BresenhamLine(normals[3][0],normals[3][1])
	# print normalEndLPoint
	lenghtPoint = BresenhamLine(lenght[0],lenght[1])
	# print lenghtPoint

	checkIntersectTangent(bresenhamIndex,tangentStartPoint,line)
	checkIntersectTangent(bresenhamIndex,tangentEndPoint,line)
	checkIntersectNormals(bresenhamIndex,normalStartRPoint,line)
	checkIntersectNormals(bresenhamIndex,normalStartLPoint,line)
	checkIntersectNormals(bresenhamIndex,normalEndRPoint,line)
	checkIntersectNormals(bresenhamIndex,normalEndLPoint,line)
	checkIntersectLine(bresenhamIndex,lenghtPoint,line)

#-----------------------------------------------------------------------

def main():
	global imgTest
	image_list = getFileName() #circleNaturalHighlight #cubeGreenUnderShadeNoon #complexSqGreenNoonLight
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/complexSqGreenNoonLight.jpg'),cv2.COLOR_BGR2RGB) 
	height,width = imgRGBcube.shape[:2]
	imgTest = np.zeros((height,width,3), np.uint8)
	imgTest = imgRGBcube[:] / 4
	# for image in image_list:
		# imgTest = np.zeros((height,width,3), np.uint8)
		# imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/' + image),cv2.COLOR_BGR2RGB)
	edgesRGBcube = auto_canny(imgRGBcube)
	im2, contours, hierarchy = cv2.findContours( edgesRGBcube.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	# print contours
	graphList = contoursToGraphList(contours)
	graphLongest = getLongestLenghtGraph(graphList)	# for graph in graphList:
		# graph.printGraph(imgTest)
	lineDict , vertexOnLineDict = graphLongest.subGraphToLineBFS(imgTest)
	# print len(lineDict)
	lineEndPointDict = makeLineDictWithEndPoints(lineDict)
	for line in lineEndPointDict:
		print lineEndPointDict[line]
		# imgTest[lineEndPointDict[line][0][1]][lineEndPointDict[line][0][0]] = (255,0,0)
		# imgTest[lineEndPointDict[line][1][1]][lineEndPointDict[line][1][0]] = (255,255,0)
	lineGraph = lineToLineVertexAndLineGraph(lineDict,lineEndPointDict)
	bresenhamIndex = {}
	while(len(lineGraph.getEdgesList()) < 20):
		for line in lineGraph.getVertices():  #>>>> O(N)
			line.growSearchLine()
			tangent,normals,lenght = line.getVertexData()
			drawAndCheckIntersectInBresenhamIndex(bresenhamIndex,line,tangent,normals,lenght)

			# print "hello"
		break


	pyplot.imshow(imgTest)
	pyplot.show()

if __name__ == "__main__":
	main()