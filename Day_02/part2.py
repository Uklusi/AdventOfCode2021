
from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

s = Position(0,0)
aim = 0

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        line = line.split()
        if line[0] == "forward":
            s += Vector(int(line[1]), aim*int(line[1]))
        elif line[0] == "up":
            aim -= int(line[1])
        elif line[0] == "down":
            aim += int(line[1])

result = s.x * s.y


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
