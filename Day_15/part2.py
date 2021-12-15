from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

origRiskLevels = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        origRiskLevels.append([int(n) for n in line])

def addToList(numList: list[int], n):
    new: list[int] = [i + n for i in numList]
    return [(n if n <= 9 else n - 9) for n in new]

def makeRow(numList: list[int]):
    new: list[int] = []
    for i in range(5):
        new.extend(addToList(numList, i))
    return new

riskLevels0 = [makeRow(row) for row in origRiskLevels]

riskLevels = []

for i in range(5):
    riskLevels.extend([addToList(row, i) for row in riskLevels0])

start = MapPosition(0, 0, frame=riskLevels)
end = MapPosition(len(riskLevels[0]) - 1, len(riskLevels) - 1, frame=riskLevels)

result = aStar(start, end, distanceFunction=lambda p, q: riskLevels[q.y][q.x])



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
