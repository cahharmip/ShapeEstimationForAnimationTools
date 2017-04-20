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

def drawApproxLine(b0,b1,leftMostPoint,rightMostPoint):
	yInit = b0 + b1*leftMostPoint
	yDes = b0 + b1*rightMostPoint
	# print "_____ Check left&right Point ______"
	firstPoint = (leftMostPoint,int(yInit))
	secondPoint = (rightMostPoint,int(yDes))
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
				drawApproxLine(line[0],line[1],leftMostPoint[0],rightMostPoint[0])
				lineEndPointDict[line] = (leftMostPoint,rightMostPoint)
	return lineEndPointDict
#-----------------------------------------------------------------------

#--------------------------- Calculation -------------------------------

#-----------------------------------------------------------------------

def main():
	global imgTest
	image_list = getFileName() #circleNaturalHighlight #cubeGreenUnderShadeNoon #complexSqGreenNoonLight
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/complexSqGreenNoonLight.jpg'),cv2.COLOR_BGR2RGB) 
	height,width = imgRGBcube.shape[:2]
	imgTest = np.zeros((height,width,3), np.uint8)
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
	print len(lineDict)
	lineEndPointDict = makeLineDictWithEndPoints(lineDict)
	lineGraph = lineToLineVertexAndLineGraph(lineDict,lineEndPointDict)
	while(len(lineGraph.getEdgesList()) < 6):
		tangentDict = {}
		NormalsDict = {}
		inLineDict = {}
		for line in lineGraph.getVertices():  #>>>> O(N)
			line.growSearchLine()
		break


	# pyplot.imshow(imgTest)
	# pyplot.show()

if __name__ == "__main__":
	main()