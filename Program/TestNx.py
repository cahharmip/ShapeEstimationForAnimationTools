import cv2
import math
import numpy as np

def BresenhamLine(start, end):

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

def checkIntersectTangent(bresenhamIndex,tangentPoint,line,height,width,graph,imgTest):
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
			if intersectType == "tangent"and not intersectLine == line:
				# print "addEdgeWithType L-Junction"
				graph.add_edge(line,intersectLine,weight="L-Junction")
			elif intersectType == "normals" and not intersectLine == line:
				# print "addEdgeWithType Collinearity"
				graph.add_edge(line,intersectLine,weight="Colinearity")
			else:
				# print "addEdgeWithType T-Junction"
				i = 0
				# graph.addEdge(line,intersectLine,"T-Junction")
		else:
			bresenhamIndex[point] = (line,"tangent")

def checkIntersectNormals(bresenhamIndex,normalsPoint,line,height,width,graph,imgTest):
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
			if intersectType == "tangent"and not intersectLine == line:
				# print "addEdgeWithType Collinearity"
				graph.add_edge(line,intersectLine,weight="Colinearity")
		else:
			bresenhamIndex[point] = (line,"normals")

def checkIntersectLine(bresenhamIndex,lenghtPoint,line,graph,imgTest):
	for point in lenghtPoint:
		if point in bresenhamIndex:
			intersectLine = bresenhamIndex[point][0]
			intersectType = bresenhamIndex[point][1]
			if intersectType == "tangent" and not intersectLine == line:
				i = 0
				# print "addEdgeWithType T-junction"
				# graph.addEdge(line,intersectLine,"T-Junction")
		else:
			bresenhamIndex[point] = (line,"normals")

class TestNx(object):
	def __init__(self):
		self.__id = 0

	def drawAndCheckIntersectInBresenhamIndexNx(self,bresenhamIndex,line,tangent,normals,lenght,height,width,graph,imgTest):
		tangentStartPoint = BresenhamLine(tangent[0][1][1],tangent[0][1][0])
		tangentEndPoint = BresenhamLine(tangent[1][1][0],tangent[1][1][1])
		normalStartRPoint = BresenhamLine(normals[0][1][0],normals[0][1][1])
		normalStartLPoint = BresenhamLine(normals[1][1][0],normals[1][1][1])
		normalEndRPoint = BresenhamLine(normals[2][1][0],normals[2][1][1])
		normalEndLPoint = BresenhamLine(normals[3][1][0],normals[3][1][1])
		lenghtPoint = BresenhamLine(lenght[0],lenght[1])

		# print graph.nodes()
		checkIntersectTangent(bresenhamIndex,tangentStartPoint,line,height,width,graph,imgTest)
		checkIntersectTangent(bresenhamIndex,tangentEndPoint,line,height,width,graph,imgTest)
		checkIntersectNormals(bresenhamIndex,normalStartRPoint,line,height,width,graph,imgTest)
		checkIntersectNormals(bresenhamIndex,normalStartLPoint,line,height,width,graph,imgTest)
		checkIntersectNormals(bresenhamIndex,normalEndRPoint,line,height,width,graph,imgTest)
		checkIntersectNormals(bresenhamIndex,normalEndLPoint,line,height,width,graph,imgTest)
		checkIntersectLine(bresenhamIndex,lenghtPoint,line,graph,imgTest)