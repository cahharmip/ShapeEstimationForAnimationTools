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
			print contour[i][0],contour[i+1][0]
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
	return index, mostDeviation

def findLSFAndMostDev(tempX,tempY,sigma,tree):
	for point in tree.data:
		# print point[0][0]
		tempX.append(point[0][0])
		tempY.append(point[0][1])
		sigma.append(1.0)
	xArray = np.array(tempX,dtype='int64')
	yArray = np.array(tempY,dtype='int64')
	sigma = np.array(sigma,dtype='int64')
	# b0,b1 = findRegression(xArray,yArray)
	# print tree.data
	# b0,b1 = initContourLinearEquation(tree.data)
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

def treeSubdividsor(tree):
	global recurRound
	recurRound+=1
	tempY = []
	tempX = []
	sigma = []
	index,mostDeviation = findLSFAndMostDev(tempX,tempY,sigma,tree)
	# cv2.drawContours(imgTest, tree.data, -1, (random.randint(50,255),random.randint(100,255),random.randint(50,255)),0)
	myDrawContour(tree.data)
	# print index
	tree.significant = mostDeviation
	leftTree = tree.data[0:index + 1]
	rightTree = tree.data[index:]
	if len(leftTree) > 1 and len(rightTree) > 1:
		tree.left = Tree(leftTree)
		# print tree.left.data

		tree.right = Tree(rightTree)
		# print tree.right.data
		# print tree.left.data

		if len(tree.left.data) >= 4 :
			treeSubdividsor(tree.left)
		# print tree.right.data
		if len(tree.right.data) >= 4 :
			treeSubdividsor(tree.right) # Problem that it not cut anymore and then he recursive like hell!!

def test():
	global imgTest
	image_list = getFileName()
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/cubeGreenUnderShadeNoon.jpg'),cv2.COLOR_BGR2RGB)
	height,width = imgRGBcube.shape[:2]
	imgTest = np.zeros((height,width,3), np.uint8)
	# imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/' + image),cv2.COLOR_BGR2RGB)
	edgesRGBcube = auto_canny(imgRGBcube)
	im2, contours, hierarchy = cv2.findContours( edgesRGBcube.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# print hierarchy
	listOfContoursList = []
	longestIndex = 0
	longestIndex = findLongestAndCreateListofContour(contours,longestIndex,listOfContoursList)
	# cv2.drawContours(imgTest,listOfContoursList , longestIndex, (255,172,255), 0)
	# print listOfContoursList[0]
	# cv2.drawContours(imgTest, testSlopeCountour, -1, (150,255,150), 0)
	treeSet = []
	groupListToTree(treeSet, listOfContoursList)
	## TEST WITH LONGESTINDEX ##
	# print treeSet[longestIndex].data
	treeSubdividsor(treeSet[longestIndex])
	print recurRound
	# traverseTreeToSelectSection(treeSet[longestIndex])

	###############################
	pyplot.imshow(imgTest)
	pyplot.show()

if __name__ == "__main__":
	test()
	# main()