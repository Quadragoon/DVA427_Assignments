import math

dataFile = open("assignment1.txt", mode="r")

line = dataFile.readline()
while line != "@data\n":
    line = dataFile.readline()

print("Found data start, processing...")

class Data:
    attributes = [0]
    classification = 0

    def __repr__(self):
        return self.attributes[9]

allData = []

for line in dataFile:
    dataPoint = Data()
    dataPoint.attributes = line.split(",")
    dataPoint.classification = dataPoint.attributes[-1]
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


print("Training set size: " + trainingSetSize.__str__())
print("Validation set size: " + validationSetSize.__str__())
print("Testing set size: " + testingSetSize.__str__())