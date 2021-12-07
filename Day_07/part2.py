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
        positions = [int(n) for n in line.split(",")]

positions.sort()

result = inf

def sumto(n):
    n = abs(n)
    return n * (n + 1) // 2

for n in range(positions[0], positions[-1] + 1):
    s = sum([sumto(n - x) for x in positions])
    result = min(result, s)





with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()

