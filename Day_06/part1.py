from AoCUtils import *


result = 0
partNumber = "1"

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
        instate = [int(n) for n in line.split(",")]

newbornQueue = []

CYCLE = 7
DELAY = 2
NREP = 80

newbornQueue = [0] * DELAY
fishQueue = [0] * CYCLE
for n in instate:
    fishQueue[n] += 1

for day in range(NREP):
    n = day % CYCLE
    newbornQueue.append(fishQueue[n])
    fishQueue[n] += newbornQueue.pop(0)

result = sum(fishQueue) + sum(newbornQueue)





with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
