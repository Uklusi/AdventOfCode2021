from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

steps = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip().split()
        turn = line[0]
        line = line[1].split(",")
        x = list(map(int, line[0][2:].split("..")))
        y = list(map(int, line[1][2:].split("..")))
        z = list(map(int, line[2][2:].split("..")))
        steps.append((turn, x, y, z))

cubes = defaultdict(lambda: False)

for step in steps:
    setCube = (True if step[0] == "on" else False)
    (x, y, z) = step[1:]
    if x[0] < -50 or x[0] > 50 or x[1] < -50 or x[1] > 50:
        continue
    for i in range(x[0], x[1] + 1):
        for j in range(y[0], y[1] + 1):
            for k in range(z[0], z[1] + 1):
                cubes[(i, j, k)] = setCube

# print(cubes)
result = sum(1 for x in cubes.values() if x)


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
