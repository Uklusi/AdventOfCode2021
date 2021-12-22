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

steps2: list[tuple[Region, StepIndex]] = [(step[0], i) for (i, step) in enumerate(steps)]

# listMins contains, for each dimension, the ordered list of lower bounds for each step,
# and the step index that lower bound comes from
# Same for listMaxs
# Type signature is list[list[tuple[Coord, StepIndex]]]
listMins = [sorted([(step[0][i][0], step[1]) for step in steps2], reverse=True) for i in range(3)]
listMaxs = [sorted([(step[0][i][1], step[1]) for step in steps2], reverse=True) for i in range(3)]

regionsep: list[list[tuple[Coord, set[StepIndex]]]] = [[], [], []]

for i in range(3):
    curr = None
    # currsteps is the set of steps s.t. their region intersects the strip
    # curr × (-inf, inf) × (-inf, inf) (or with y or z depending on i)
    currsteps: set[StepIndex] = set()
    while len(listMaxs[i]) > 0:
        if len(listMins[i]) == 0:
            newTransition = listMaxs[i].pop()
            insert = False
        else:
            newTransition = listMins[i][-1]
            if newTransition[0] > listMaxs[i][-1][0]:
                newTransition = listMaxs[i].pop()
                insert = False
            else:
                newTransition = listMins[i].pop()
                insert = True
        # if newTransition comes from Mins, then we need to add the step to the set
        # otherwise we need to remove it

        if insert:
            currsteps.add(newTransition[1])
        else:
            currsteps.remove(newTransition[1])

        new = newTransition[0]
        if curr is None or curr < new:
            regionsep[i].append((new, currsteps.copy()))
            curr = new
        elif curr == new:
            regionsep[i][-1] = (new, currsteps.copy())
        else:
            raise Exception("Value Error")
# At the end, for each axis we have a list of (coord, s) s.t.
# the set of steps intersecting with the strip is exactly s, and that is true
# for all coords up to the next one in the list

# regions is the complete list of regions to be considered. Each region is non-overlapping,
# contained is exactly one of the inctersections of all regions coming from the original steps,
# and it is saved as its volume and the last step acting on the region (which is the only one that matters)
# Actually it's a generator, because there are 198_360_483 regions and storing them in memory it's not worth

# Hold on a sec, I wanna try using a for loop
# This is quicker, but it's functionally equivalent to the code below
for x in zip(regionsep[0], regionsep[0][1:]):
    for y in zip(regionsep[1], regionsep[1][1:]):
        for z in zip(regionsep[2], regionsep[2][1:]):
            s = x[0][1] & y[0][1] & z[0][1]
            if len(s) > 0 and steps[max(s)][1]:
                result += (x[1][0] - x[0][0]) * (y[1][0] - y[0][0]) * (z[1][0] - z[0][0])

# regions = (
#     (
#         (x[1][0] - x[0][0]) * (y[1][0] - y[0][0]) * (z[1][0] - z[0][0]),
#         max(x[0][1] & y[0][1] & z[0][1])
#     )
#     for x in zip(regionsep[0], regionsep[0][1:])
#     for y in zip(regionsep[1], regionsep[1][1:])
#     for z in zip(regionsep[2], regionsep[2][1:])
#     if len(x[0][1] & y[0][1] & z[0][1]) > 0
# )

# for region in regions:
#     stepIndex = region[1]
#     if steps[stepIndex][1]:
#         result += region[0]

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
