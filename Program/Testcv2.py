import cv2
import math
import random
from TesTree import Tree
import numpy as np
import subprocess
import scipy.optimize as optimization
from matplotlib import pyplot

imgTest = 0
recurRound = 0

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

def searchEdgePointToLine(edged):
	return 0

def myDrawContour(contour):
	# print contour
	a,b,c = random.randint(0,255),random.randint(0,255),random.randint(0,255)
	for i in range(len(contour)):
		if i != len(contour) - 1:
			# print contour[i][0],contour[i+1][0]	
			cv2.line(imgTest,(contour[i][0][0],contour[i][0][1]),(contour[i+1][0][0],contour[i+1][0][1]),(a,b,c),0)
		
def groupListToTree(treeSet, listOfContoursList):
	x = 0
	for i in range (len(listOfContoursList)):
		treeSet.append(Tree(listOfContoursList[i]))

def euclidianDistance(point1,point2):
	x1 = point1[0][0]
	x2 = point2[0][0]
	y1 = point1[0][1]
	y2 = point2[0][1]
	dist = abs(math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2)))
	return dist

def initContourLinearEquation(contour):
	initPointMost = contour[0];
	destPointMost = contour[-1];
	b1 = ( destPointMost[0][1] - initPointMost[0][1] ) / ( destPointMost[0][0] - initPointMost[0][0] )
	b0 = initPointMost[0][1] -  b1*initPointMost[0][0]
	return b1, b0

def LSFWithPerpendicularOffset(xArray,yArray):
	#y = b0 + b1x with di = abs(yi - (b0+b1(xi)))/math.sqrt(1 + b1^2)
	sumX = sum(xArray)
	sumY = sum(yArray)
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
	B_uprightEq = sumX2 - math.pow(sumX,2)/n
	B_botEq = ((sumX*sumY)/n) - sumXY
	B = 0.5*(B_upleftEq - B_uprightEq)/B_botEq

	if B < 0:
		b1 = -B + math.sqrt(math.pow(B,2)+1)
	else:
		b1 = -B - math.sqrt(math.pow(B,2)+1)
	b0 = (sumY - sumX*b1)/n
	
	
	# cv2.line(imgTest,firstPoint,secondPoint,(255,255,255),0)
	return b0,b1

def findLongestAndCreateListofContour(contours,longestIndex,listOfContoursList):
	i = 0
	for index in range(len(contours)) :
		contoursList = []
		contoursLength = len(contours[index])
		if i > 155:
			i = 0
		if contoursLength >= 4:
			# cv2.drawContours(imgTest, contours, index, (i+50,i+100,i+80), 0)
			for a in range(contoursLength) : 
					# its an Array of Array of Array [[[]]]
				contoursList.append([contours[index][a][0]])
				if len(contoursList) > 4:
					if np.array_equal(contoursList[-3], contoursList[-2]):
						if np.array_equal(contoursList[-4], contoursList[-1]):
							contoursList.pop()
							break

		if contoursList != []:
			listOfContoursList.append(np.array(contoursList))
			if contoursLength > len(listOfContoursList[longestIndex]):
				longestIndex = len(listOfContoursList) - 1
				# print contoursLength , listOfContoursList[longestIndex]
		i+=1
	return longestIndex

def mostDeviationIndex(b0,b1,xArray,yArray):
	mostDeviation = 0
	index = 0
	for i in range(len(xArray)):
		dist = abs(yArray[i] - (b0 + b1*xArray[i]))/math.sqrt(1+math.pow(b1,2))
		# print yApprox , yArray[i]
		if mostDeviation < dist:
			mostDeviation = dist
			index = i
			# print mostDeviation
	xArraySorted = np.sort(xArray)
	# print xArraySorted
	#Test Draw approx line#
	yInit = b0 + b1*100
	yDes = b0 + b1*800
	if math.isnan(yInit) :
		yInit = 1
	if math.isnan(yDes) :
		yDes = 1
	firstPoint = (100,int(yInit))
	secondPoint = (800,int(yDes))
	#######################
	return index, mostDeviation , firstPoint, secondPoint

def findLSFAndMostDev(tempX,tempY,sigma,tree):
	for point in tree.data:
		# print point[0][0]
		tempX.append(point[0][0])
		tempY.append(point[0][1])
		sigma.append(1.0)
	xArray = np.array(tempX,dtype='int64')
	yArray = np.array(tempY,dtype='int64')
	sigma = np.array(sigma,dtype='int64')
	b0,b1 = LSFWithPerpendicularOffset(xArray,yArray)
	return mostDeviationIndex(b0,b1,xArray,yArray)

def traverseTreeToSelectSection(tree):
	print tree.data
	print tree.significant
	# cv2.drawContours(imgTest, tree.data, -1, (random.randint(50,255),random.randint(100,255),random.randint(50,255)),0)

	if tree.left != None:
		traverseTreeToSelectSection(tree.left)

	if tree.right != None:
		traverseTreeToSelectSection(tree.right)

	return "Select the lowest Deviation straight line on every side"

def treeSubdividsor(tree,height,width):
	global recurRound
	global imgTest
	recurRound+=1
	tempY = []
	tempX = []
	sigma = []
	index,mostDeviation,firstPoint,secondPoint = findLSFAndMostDev(tempX,tempY,sigma,tree)
	myDrawContour(tree.data)
	# cv2.line(imgTest,firstPoint,secondPoint,(255,255,255),0)
	
	# print "TreeData", tree.data[0] , tree.data[-1]
	tree.significant = mostDeviation
	leftTree = tree.data[0:index ]
	# print "LeftTree",len(leftTree), leftTree[0] if len(leftTree) > 1 else "endtree" , leftTree[-1] if len(leftTree) > 1 else "endtree"
	rightTree = tree.data[index + 1 :]
	# print "RightTree",len(rightTree), rightTree[0] if len(rightTree) > 1 else "endtree" ,rightTree[-1] if len(rightTree) > 1 else "endtree"
	# print "___________"
	if len(leftTree) > 1 :
		tree.left = Tree(leftTree)
		if len(tree.left.data) >= 4 :
			treeSubdividsor(tree.left,height,width)
		
	if len(rightTree) > 1 :
		tree.right = Tree(rightTree)
		if len(tree.right.data) >= 4 :
			treeSubdividsor(tree.right,height,width)
	
def reconstuctContourList(contour):
	used = {}
	rangeX = {'min': 99999 , 'max' : -1}
	rangeY = {'min': 99999 , 'max' : -1}
	newContour = []
	for point in contour:
		if rangeX['min'] > point[0][0]:
			rangeX['min'] = point[0][0]
		if rangeX['max'] < point[0][0]:
			rangeX['max'] = point[0][0]

		if rangeY['min'] > point[0][1]:
			rangeY['min'] = point[0][1]
		if rangeY['max'] < point[0][1]:
			rangeY['max'] = point[0][1]

		if np.array_str(point) not in used:
			# if point[0][0]
			used[np.array_str(point)] = 1
			newContour.append(point)

	myDrawContour(newContour)

	return newContour

def test():
	global imgTest
	image_list = getFileName()
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/cubeGreenUnderShadeNoon.jpg'),cv2.COLOR_BGR2RGB)
	height,width = imgRGBcube.shape[:2]
	imgTest = np.zeros((height,width,3), np.uint8)
	# imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/' + image),cv2.COLOR_BGR2RGB)
	edgesRGBcube = auto_canny(imgRGBcube)
	im2, contours, hierarchy = cv2.findContours( edgesRGBcube.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	listOfContoursList = []
	longestIndex = 0
	longestIndex = findLongestAndCreateListofContour(contours,longestIndex,listOfContoursList)

	treeSet = []
	groupListToTree(treeSet, listOfContoursList)
	## TEST WITH LONGESTINDEX ##
 	reconstuctContourList(treeSet[longestIndex].data)
	# treeSubdividsor(treeSet[longestIndex],height,width)

	print recurRound
	pyplot.imshow(imgTest)
	pyplot.show()

	###############################
	
if __name__ == "__main__":
	test()
	# main()