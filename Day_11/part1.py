from collections import deque
from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = True
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

levels = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        levels.append([int(n) for n in list(line)])

NUMSTEPS = 100

def rangeFrame(frame, x=False, y=False):
    if x:
        return range(len(frame[0]))
    if y:
        return range(len(frame))
    return product(range(len(frame[0])), range(len(frame)))

for _ in range(NUMSTEPS):
    updatequeue = deque()
    flashes = defaultdict(lambda: False)
    for (x, y) in rangeFrame(levels):
        updatequeue.append(MapPosition(x, y, frame=levels))
        levels[y][x] += 1
    while len(updatequeue) > 0:
        p = updatequeue.popleft()
        if flashes[p]:
            levels[p.y][p.x] = 0
        if levels[p.y][p.x] > 9:
            flashes[p] = True
            result += 1
            levels[p.y][p.x] = 0
            for q in p.adjacent(includeCorners=True):
                updatequeue.append(q)
                levels[q.y][q.x] += 1



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
