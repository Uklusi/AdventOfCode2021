from AoCUtils import *
from collections import defaultdict

result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

straightLines = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        [startStr, endStr] = line.split(" -> ")
        startPos = Position(*[int(n) for n in startStr.split(",")])
        endPos = Position(*[int(n) for n in endStr.split(",")])
        if (endPos - startPos).direction() in [Vector(0, 1), Vector(0, -1), Vector(1, 0), Vector(-1, 0)]:
            straightLines.append((startPos, endPos))

numLines = defaultdict(lambda: 0)

for (start, end) in straightLines:
    numLines[start] += 1
    v = (end - start).direction()
    scroll = start
    while scroll != end:
        scroll += v
        numLines[scroll] += 1

result = sum([1 for n in numLines.values() if n > 1])



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()

