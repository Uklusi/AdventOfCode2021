from AoCUtils import *

writeToLog = False
# writeToLog = True

useExample = False
# useExample = True


result = 0
partNumber = "1"

if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

timer_start(partNumber)

rightMoving = set()
downMoving = set()

inputFileName = ("example.txt" if useExample else "input.txt")
with open(inputFileName, "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for (y, line) in enumerate(lines):
        line = line.strip()
        for (x, char) in enumerate(line):
            if char == ">":
                rightMoving.add((x, y))
            elif char == "v":
                downMoving.add((x, y))

xLimit = len(lines[0])
yLimit = len(lines)

def step(rightMoving, downMoving):
    newRightMoving = set()
    newDownMoving = set()
    hasMoved = False
    for (x, y) in rightMoving:
        newX = x + 1
        if newX == xLimit:
            newX = 0
        newPos = (newX, y)
        if newPos in rightMoving or newPos in downMoving:
            newRightMoving.add((x, y))
        else:
            newRightMoving.add(newPos)
            hasMoved = True
    for (x, y) in downMoving:
        newY = y + 1
        if newY == yLimit:
            newY = 0
        newPos = (x, newY)
        if newPos in newRightMoving or newPos in downMoving:
            newDownMoving.add((x, y))
        else:
            newDownMoving.add(newPos)
            hasMoved = True

    return (newRightMoving, newDownMoving, hasMoved)

flag = True
n = 0
while flag:
    n += 1
    (rightMoving, downMoving, flag) = step(rightMoving, downMoving)

result = n

timer_stop(partNumber)

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
