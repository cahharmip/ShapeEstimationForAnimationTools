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

	def traverseAndAssignEdge(self):
		
		return 0