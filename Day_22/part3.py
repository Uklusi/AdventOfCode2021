from itertools import starmap
from math import prod
from AoCUtils import *

useExample = False
# useExample = True

result = 0
partNumber = "3"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

timer_start()

Coord = int
Limit = tuple[Coord, Coord]
Region = tuple[Limit, Limit, Limit]
StepIndex = int


steps: list[tuple[Region, bool]] = []

inputFileName = ("example.txt" if useExample else "input.txt")
with open(inputFileName, "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        (newState, limitsString) = line.strip().split()
        limits = limitsString.split(",")
        turn = (True if newState == "on" else False)

        c: list[Limit] = []
        for i in range(3):
            (a, b) = limits[i][2:].split("..")
            c.append((int(a), int(b) + 1))
        steps.append((tuple(c), turn))

def intersect(a: Region, b: Region) -> Optional[Region]:
    ret: Region = tuple((
        max(a[i][0], b[i][0]),
        min(a[i][1], b[i][1])
    ) for i in range(3))
    if any(ret[i][0] >= ret[i][1] for i in range(3)):
        return None
    else:
        return ret

def subtract(a: Region, b: Region, keepSecondIfContained) -> tuple[bool, list[Region]]:
    inters = intersect(a, b)
    if inters is None:
        return (False, [a])
    if inters == b:
        if keepSecondIfContained:
            return (True, [a])
        else:
            return (False, [])

    ret: list[Region] = []

    ((x1, x2), (y1, y2), (z1, z2)) = inters
    (x, y, z) = a

    if x1 != x[0]:
        ret.append(((x[0], x1), y, z))
    if x2 != x[1]:
        ret.append(((x2, x[1]), y, z))
    if y1 != y[0]:
        ret.append(((x1, x2), (y[0], y1), z))
    if y2 != y[1]:
        ret.append(((x1, x2), (y2, y[1]), z))
    if z1 != z[0]:
        ret.append(((x1, x2), (y1, y2), (z[0], z1)))
    if z2 != z[1]:
        ret.append(((x1, x2), (y1, y2), (z2, z[1])))

    return (False, ret)

finalRegionList: list[Region] = []
for step in steps:
    (newRegion, add) = step
    newRegionList: list[Region] = []
    isAlreadyAdded = False
    for region in finalRegionList:
        (isAdded, decomposition) = subtract(region, newRegion, add)
        if isAdded:
            isAlreadyAdded = True
        newRegionList.extend(decomposition)
    if not isAlreadyAdded and add:
        newRegionList.append(newRegion)
    finalRegionList = newRegionList

for region in finalRegionList:
    result += prod(region[i][1] - region[i][0] for i in range(3))



timer_stop()

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
