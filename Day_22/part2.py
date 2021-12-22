from itertools import starmap
from math import prod
from AoCUtils import *

useExample = False
# useExample = True

result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

steps = []

class Lim(NamedTuple):
    min: int
    max: int

class Range(NamedTuple):
    x: Lim
    y: Lim
    z: Lim

inputFileName = ("example.txt" if useExample else "input.txt")
with open(inputFileName, "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip().split()
        turn = line[0]
        line = line[1].split(",")
        turn = (True if turn == "on" else False)
        x = Lim(*map(int, line[0][2:].split("..")))
        x = Lim(x.min, x.max + 1)
        y = Lim(*map(int, line[1][2:].split("..")))
        y = Lim(y.min, y.max + 1)
        z = Lim(*map(int, line[2][2:].split("..")))
        z = Lim(z.min, z.max + 1)
        steps.append(((x, y, z), turn))

steps2 = [(step[0], i) for (i, step) in enumerate(steps)]


listMins = [sorted([(step[0][i].min, step[1]) for step in steps2]) for i in range(3)]
listMaxs = [sorted([(step[0][i].max, step[1]) for step in steps2]) for i in range(3)]

regionsep = [[], [], []]
for i in range(3):
    curr = None
    currsteps = set()
    while len(listMaxs[i]) > 0:
        if len(listMins[i]) == 0:
            new = listMaxs[i].pop(0)
            insert = False
        else:
            new = listMins[i][0]
            if new[0] > listMaxs[i][0][0]:
                new = listMaxs[i].pop(0)
                insert = False
            else:
                new = listMins[i].pop(0)
                insert = True

        if insert:
            currsteps.add(new[1])
        else:
            currsteps.remove(new[1])
        new = new[0]
        if curr is None or curr < new:
            regionsep[i].append((new, currsteps.copy()))
            curr = new
        elif curr == new:
            regionsep[i][-1] = (new, currsteps.copy())
        else:
            raise Exception("Value Error")

# print([len(regionsep[i]) for i in range(3)])
# Generator to go around the memory issue
regions = (
    (
        (x[1][0] - x[0][0]) * (y[1][0] - y[0][0]) * (z[1][0] - z[0][0]),
        max(x[0][1] & y[0][1] & z[0][1])
    )
    for x in zip(regionsep[0], regionsep[0][1:])
    for y in zip(regionsep[1], regionsep[1][1:])
    for z in zip(regionsep[2], regionsep[2][1:])
    if len(x[0][1] & y[0][1] & z[0][1]) > 0
)

for region in regions:
    stepIndex = region[1]
    if steps[stepIndex][1]:
        result += region[0]

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
