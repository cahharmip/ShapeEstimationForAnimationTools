import cv2
import math
import numpy as np

class LineGraph(object):
	def __init__(self, graphDict = None):
		if graphDict == None:
			graphDict = {}
		self.__graphDict = graphDict
		self.__vertexOnLineDict = {}
		self.__edgeList = {}

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

	def hasVertex(self,vertex):
		if vertex not in self.__graphDict:
			return True
		else :
			return False

	def addVertex(self,lineVertex):
			self.__graphDict[lineVertex] = []

	def addEdge(self,line1,line2,junctionType): # Edge will have { (line1,line2) : type of junction}
		#edge is in list form.
		if line1 in self.__graphDict:
			if line2 not in set(self.__graphDict[line1]):
				self.__graphDict[line1].append((line2,junctionType))
		else:
			self.__graphDict[line1] = [(line2,junctionType)]
		if line1 not in set(self.__graphDict[line2]):
			self.__graphDict[line2].append((line1,junctionType))

	def traverseAndAssignEdge(self):
		return 0