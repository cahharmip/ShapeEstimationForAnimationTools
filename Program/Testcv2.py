import cv2
from TesTree import Tree
import numpy as np
import subprocess
import scipy.optimize as optimization
from matplotlib import pyplot

imgTest = np.zeros((852, 1136), np.uint16)

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

def groupListToTree(treeSet, listOfContoursList):
	x = 0
	for i in listOfContoursList:
		treeSet.append(Tree(i))

def findRegression(xArray,yArray):
	sumX = sum(xArray)
	sumY = sum(yArray)
	sumXY = 0.0
	sumX2 = 0.0
	sumY2 = 0.0
	b0 = 0.0
	b1 = 0.0
	size = len(xArray)
	for i in range(size):
		sumXY += xArray[i] * yArray[i]
		sumX2 += xArray[i] * xArray[i]
		sumY2 += yArray[i] * yArray[i]
	b0 = ((sumY*sumX2)-(sumX*sumXY))/((size*sumX2)-(sumX*sumX))
	b1 = ((size*sumXY)-(sumX*sumY))/((size*sumX2)-(sumX*sumX))
	return b0,b1

def arrayToContour():
	return "contour format"

def mostDeviationIndex(b0,b1,xArray,yArray):
	mostDeviation = 0
	index = 0
	for i in range(len(xArray)):
		yApprox = xArray[i] * b1 + b0
		dif = abs(yApprox - yArray[i])
		# print yApprox , yArray[i]
		if mostDeviation < dif:
			mostDeviation = dif
			index = i
			# print mostDeviation
	return index, mostDeviation

def findIndexAndMostDev(tempX,tempY,sigma,tree):
	for point in tree.data:
		# print point[0][0]
		tempX.append(point[0][0])
		tempY.append(point[0][1])
		sigma.append(1.0)
	xArray = np.array(tempX,dtype='int64')
	yArray = np.array(tempY,dtype='int64')
	sigma = np.array(sigma,dtype='int64')
	b0,b1 = findRegression(xArray,yArray)
	return mostDeviationIndex(b0,b1,xArray,yArray)


def traverseTreeToSelectSection(tree):
	print tree.data
	print tree.significant
	cv2.drawContours(imgTest, tree.data, 0, (255,255,0),0)

	if tree.left != None:
		traverseTreeToSelectSection(tree.left)

	if tree.right != None:
		traverseTreeToSelectSection(tree.right)

	return "Select the lowest Deviation straight line on every side"

def treeSubdividsor(tree):
		tempY = []
		tempX = []
		sigma = []
		index,mostDeviation = findIndexAndMostDev(tempX,tempY,sigma,tree)
		# print index
		tree.significant = mostDeviation
		leftTree = tree.data[0:index + 1]
		# print leftTree
		tree.left = Tree(leftTree)
		# print tree.left.data
		print len(tree.left.data)
		if len(tree.left.data) >= 4 :
			treeSubdividsor(tree.left)

		rightTree = tree.data[index:]
		tree.right = Tree(rightTree)
		print tree.right.data
		# print tree.right.data
		if len(tree.right.data) >= 4 :
			treeSubdividsor(tree.right) # Problem that it not cut anymore and then he recursive like hell!!

def test():
	image_list = getFileName()
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/cubeGreenUnderShadeNoon.jpg'),cv2.COLOR_BGR2RGB)
	# imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/' + image),cv2.COLOR_BGR2RGB)
	edgesRGBcube = auto_canny(imgRGBcube)
	im2, contours, hierarchy = cv2.findContours( edgesRGBcube.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# print hierarchy
	i = 0
	x = 0
	listOfContoursList = []
	longestIndex = 0
	for index in range(len(contours)) :
		contoursList = []
		contoursLength = len(contours[index])
		if i > 255:
			i = 0
		if contoursLength >= 4:
			# cv2.drawContours(imgTest, contours, index, (i,i,i), 0)
			for a in range(contoursLength) : 
				# its an Array of Array of Array [[[]]]
				contoursList.append([contours[index][a][0]])

		if contoursList != []:
			listOfContoursList.append(np.array(contoursList))
			if contoursLength > len(listOfContoursList[longestIndex]):
				longestIndex = len(listOfContoursList) - 1
				# print contoursLength , listOfContoursList[longestIndex]
		i+=1	
	# cv2.drawContours(imgTest,listOfContoursList , longestIndex, (255,255,255), 3)

	
	treeSet = []
	groupListToTree(treeSet, listOfContoursList)
	## TEST WITH LONGESTINDEX ##
	# print treeSet[0].data
	treeSubdividsor(treeSet[1])
	# if i > 255:
	
	# 	i = 0
	traverseTreeToSelectSection(treeSet[1])

	###############################
	pyplot.imshow(imgTest)
	pyplot.show()

if __name__ == "__main__":
	test()
	# main()