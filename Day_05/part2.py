from AoCUtils import *
from collections import defaultdict

result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

ventLines = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        [startStr, endStr] = line.split(" -> ")
        startPos = Position(*[int(n) for n in startStr.split(",")])
        endPos = Position(*[int(n) for n in endStr.split(",")])
        ventLines.append((startPos, endPos))

numLines = defaultdict(lambda: 0)

for (start, end) in ventLines:
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

