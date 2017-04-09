def linearRegression(xArray,yArray):
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