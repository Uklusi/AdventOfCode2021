from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

riskLevels = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        riskLevels.append([int(n) for n in line])

start = MapPosition(0, 0, frame=riskLevels)
end = MapPosition(len(riskLevels[0]) - 1, len(riskLevels) - 1, frame=riskLevels)

result = aStar(start, end, distanceFunction=lambda p, q: riskLevels[q.y][q.x])



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
