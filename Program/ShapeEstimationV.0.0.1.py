import cv2
import math
import random
from TesTree import Tree
import numpy as np
import subprocess
import scipy.optimize as optimization
from matplotlib import pyplot

sumX = {}
sumY = {}
sumXY = {}
sumX2 = {}
sumY2 = {}

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

def myDrawContour(contour):
	# print contour
	a,b,c = random.randint(0,255),random.randint(0,255),random.randint(0,255)
	for i in range(len(contour)):
		if i != len(contour) - 1:
			# print contour[i][0],contour[i+1][0]
			cv2.line(imgTest,(contour[i][0][0],contour[i][0][1]),(contour[i+1][0][0],contour[i+1][0][1]),(a,b,c),0)

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

def preSumValue(contourList,sumX,sumY,sumXY,sumX2,sumY2):
	sumXn = 0.0
	sumYn = 0.0
	sumXYn = 0.0
	sumX2n = 0.0
	sumY2n = 0.0
	k = 0
	for i in range(len(contourList)):
		for j in range(i+1,len(contourList)):
			sumXandY = [sum(i) for i in zip(*contourList[i:j+1][0])]
	print sumXandY
	# sumY[(np.array_str(contourList[i][0]),np.array_str(contourList[j][0]))] = sumYn
	# sumXY[(np.array_str(contourList[i][0]),np.array_str(contourList[j][0]))] = sumXYn
	# sumX2[(np.array_str(contourList[i][0]),np.array_str(contourList[j][0]))] = sumX2n
	# sumY2[(np.array_str(contourList[i][0]),np.array_str(contourList[j][0]))] = sumY2n

	print 'success'

def LSFWithPerpendicularOffset(contourList):

	b0 = 0
	b1 = 0
	n = len(contourList)
	for point in contourList:
		sumX += point[0][0]
		sumY += point[0][1]
		sumXY += point[0][0] * point[0][1]
		sumX2 += point[0][0] * point[0][0]
		sumY2 += point[0][1] * point[0][1]

	B_upleftEq = sumY2 - math.pow(sumY,2)/n
	# print 'B_upleftEq' , B_upleftEq
	B_uprightEq = sumX2 - math.pow(sumX,2)/n
	# print 'B_uprightEq' , B_uprightEq
	B_botEq = ((sumX*sumY)/n) - sumXY
	# print 'B_botEq', B_botEq
	B = 0.5*(B_upleftEq - B_uprightEq)/B_botEq
	# print 'B' ,B

	if B < 0:
		b1 = -B + math.sqrt(math.pow(B,2)+1)
	else:
		b1 = -B - math.sqrt(math.pow(B,2)+1)
	b0 = (sumY - sumX*b1)/n
	
	return b0,b1

def findLSFAndMostDev(contourList):
	b0,b1 = LSFWithPerpendicularOffset(contourList)
	return deviationIndex(contourList,b0,b1)

def deviationIndex(contourList,b0,b1):
	error = 0
	for point in contourList:
		error += abs(point[0][1] - (b0 + b1*point[0][0]))/math.sqrt(1+math.pow(b1,2))
	return error

def reconstuctContourList(contour):
	used = {}
	newContour = []
	for point in contour:
		if np.array_str(point) not in used:
			# if point[0][0]
			used[np.array_str(point)] = 1
			newContour.append(point)
	# newContour.sort(key=lambda x:x[0][0])
	# print newContour
	myDrawContour(newContour)
	return newContour

def findErrorAllPairs(contourList):
	print len(contourList)
	# e = {}
	# for i in range(len(contourList)):
	# 	for j in range(i + 1, len(contourList)):
	# 		e[(i, j)] = ...
	e = {}
	k = 0
	for i in range(len(contourList)):
		for j in range(i+1,len(contourList)):
			if abs(i - j) > 10:
				e[(i,j)] = findLSFAndMostDev(contourList[i:j])
				k+=1
				if k%5000 == 0:
					print k
	return e

def segmentLeastSquare(contourList):
	opt = np.zeros(len(contourList))	
	print findErrorAllPairs(contourList)
	
def main():
	global imgTest
	image_list = getFileName()
	imgRGBcube = cv2.cvtColor(cv2.imread('Test_picture/cubeGreenUnderShadeNoon.jpg'),cv2.COLOR_BGR2RGB)
	height,width = imgRGBcube.shape[:2]
	imgTest = np.zeros((height,width,3), np.uint8)
	edgesRGBcube = auto_canny(imgRGBcube)
	im2, contours, hierarchy = cv2.findContours( edgesRGBcube.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	#contour is list(array,array,...) // [[[x1,y1]] ... [[xn,yn]]]
	listOfContoursList = []
	longestIndex = 0
	longestIndex = findLongestAndCreateListofContour(contours,longestIndex,listOfContoursList)

	reconstuctContourList(listOfContoursList[longestIndex])
	# print testContour[:][:5][0]
	preSumValue(listOfContoursList[longestIndex],sumX,sumY,sumXY,sumX2,sumY2)
	# segmentLeastSquare(listOfContoursList[longestIndex])
	pyplot.imshow(imgTest)
	pyplot.show()

if __name__ == "__main__":
	main()