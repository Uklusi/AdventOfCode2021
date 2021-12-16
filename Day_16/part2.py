from functools import reduce
from math import prod
from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)


with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        binInput = join([bin(int(n, 16))[2:].zfill(4) for n in line])

def parsePackage(package, position, acc):
    # packVer = int(package[position:position + 3], 2)
    acc = 0
    packId = int(package[position + 3:position + 6], 2)
    position = position + 6
    # printLog(f"packVer: {packVer}, packId: {packId}, position: {position}")

    if packId == 4:
        bitGroup = None
        value = ""
        while bitGroup is None or bitGroup[0] == "1":
            bitGroup = package[position:position + 5]
            position = position + 5
            value += bitGroup[1:]
        return (position, int(value, 2))

    lengthType = package[position]
    position = position + 1
    length = None
    numPacks = None
    if lengthType == "0":
        length = int(package[position:position + 15], 2)
        position = position + 15
    else:
        numPacks = int(package[position:position + 11], 2)
        position = position + 11

    newPosition = position
    countPackages = 0
    valueList = []
    while (newPosition - position != length) and (countPackages != numPacks):
        (newPosition, acc) = parsePackage(package, newPosition, acc)
        valueList.append(acc)
        countPackages += 1

    match packId:
        case 0:
            return (newPosition, sum(valueList))
        case 1:
            return (newPosition, prod(valueList))
        case 2:
            return (newPosition, min(valueList))
        case 3:
            return (newPosition, max(valueList))
        case 5:
            return (newPosition, int(valueList[0] > valueList[1]))
        case 6:
            return (newPosition, int(valueList[0] < valueList[1]))
        case 7:
            return (newPosition, int(valueList[0] == valueList[1]))
        case _:
            raise(Exception("ValueError"))


(_, result) = parsePackage(binInput, 0, 0)


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
