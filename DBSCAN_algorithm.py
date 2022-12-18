import sys
import random
import math
from ast import literal_eval

#DBScan Implementation

#Distance functions
'''
def EuclideanDistance(P,Q):
    intermediateValues = []
    for i in range(len(P[2])):
        intermediateValues.append(math.pow(Q[2][i]-P[2][i],2))
    return math.sqrt(sum(intermediateValues))
'''

#If using this then correct dbscan and FindNeighbours to have a param to differentiate the distance methods.
def MaximumDistance(P,Q):
    intermediateValues = []
    for i in range(len(P[2])):
        intermediateValues.append(abs(Q[2][i]-P[2][i]))
    return max(intermediateValues)


#Finds all neighbor points for a chosen point
def FindNeighbours(Point, Points, eps):
    tempNeighbours = []
    for y in range(len(Points)):
        for x in range(len(Points[0])):
            if MaximumDistance(Point, Points[y][x]) <= eps:
                    tempNeighbours.append(Points[y][x])
#Note: use Max Distance if required 
    return tempNeighbours

#reads vector array, performs dbscan and outputs vector array
def dbscan(vectors: list, minpts: int, epsilon: int) -> list:
    #Initialization
    pointsArray = []
    for y in range(len(vectors)):
        pointsArray.append([])
        for x in range(len(vectors[0])):
            pointsArray[y].append([y,x,vectors[y][x],"Undefined"])
            
    #DBSCAN clustering
    clusterCounter = 0
    for y in range(len(vectors)):
        for x in range(len(vectors[0])):
            if pointsArray[y][x][-1] != "Undefined":
                continue

            Neighbours = FindNeighbours(pointsArray[y][x], pointsArray, epsilon)
            if len(Neighbours) < minpts:
                pointsArray[y][x][-1] = "Noise"
                continue

            clusterCounter = clusterCounter + 1
            pointsArray[y][x][-1] = str(clusterCounter)
            if pointsArray[y][x] in Neighbours:
                Neighbours.remove(pointsArray[y][x])

            for innerPoint in Neighbours:
                if innerPoint[-1] == "Noise":
                    pointsArray[innerPoint[0]][innerPoint[1]][-1] = str(clusterCounter)
                if innerPoint[-1] != "Undefined":
                    continue
                pointsArray[innerPoint[0]][innerPoint[1]][-1] = str(clusterCounter)
                NeighboursInner = FindNeighbours(innerPoint, pointsArray, epsilon)
                if len(NeighboursInner) >= minpts:
                    Neighbours.append(NeighboursInner)
                    
                   
    #Get distinct clusters
    clusterNumbers = []
    for y in range(len(vectors)):
        for x in range(len(vectors[0])):
            if pointsArray[y][x][-1] not in clusterNumbers:
                clusterNumbers.append(pointsArray[y][x][-1])
    #Map cluster's averages
    averagesForClusters = []
    for item in clusterNumbers:
        n = 0
        vectorTemps = [0]*len(pointsArray[0][0][2])
        for y in range(len(vectors)):
            for x in range(len(vectors[0])):
                if pointsArray[y][x][-1] == item:
                    for i in range(len(pointsArray[y][x][2])):
                        vectorTemps[i] = vectorTemps[i] + pointsArray[y][x][2][i]
                    n = n + 1
        #Check Zero division
        for i in range(len(vectorTemps)):
            if vectorTemps[i] != 0:
                vectorTemps[i] = vectorTemps[i]/n
        averagesForClusters.append(vectorTemps)
    #Build clustered array and change cluster averages with initial values
    clusteredVectors = []
    for y in range(len(pointsArray)):
        clusteredVectors.append([])
        for x in range(len(pointsArray[0])):
            clusteredVectors[y].append(averagesForClusters[clusterNumbers.index(pointsArray[y][x][-1])])
    return clusteredVectors