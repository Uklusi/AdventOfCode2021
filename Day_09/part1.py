from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

heights = {}

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for (y, line) in enumerate(lines):
        line = line.strip()
        for (x, char) in enumerate(line):
            heights[Position(x, y)] = int(char)

for (x, y) in product(range(len(lines[0])), range(len(lines))):
    p = MapPosition(x, y, frame=lines)
    m = min([heights[q] for q in p.adjacent()])
    if heights[p] < m:
        result += heights[p] + 1





with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
