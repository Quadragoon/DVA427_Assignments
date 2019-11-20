import math
import numpy as np

dataFile = open("assignment1.txt", mode="r")

line = dataFile.readline()
while line != "@data\n":
    line = dataFile.readline()

print("Found data start, processing...")

class Data:
    attributes = []
    classification = 0

    def __str__(self):
        return "CLASS: " + self.classification.__str__() + "   " + "".join(self.attributes.__str__())

allData = []

for line in dataFile:
    dataPoint = Data()
    dataPoint.attributes = list(map(float, line.split(",")))
    dataPoint.classification = int(dataPoint.attributes[-1])
    del dataPoint.attributes[-1]
    allData.append(dataPoint)

dataCount = len(allData)
print("Total number of data points: " + dataCount.__str__())

trainingSetSize = math.ceil(dataCount*0.75)
trainingSet = allData[0:trainingSetSize]

validationSetSize = math.floor(dataCount*0.15)
validationSet = allData[trainingSetSize:trainingSetSize+validationSetSize]

testingSetSize = math.floor(dataCount*0.1)
testingSet = allData[trainingSetSize+validationSetSize:trainingSetSize+validationSetSize+testingSetSize]

print("trainingSetSize: " + trainingSetSize.__str__())
print("len(trainingSet): " + len(trainingSet).__str__())
print("validationSetSize: " + validationSetSize.__str__())
print("len(validationSet): " + len(validationSet).__str__())
print("testingSetSize: " + testingSetSize.__str__())
print("len(testingSet): " + len(testingSet).__str__())

for item in allData:
    print(item)