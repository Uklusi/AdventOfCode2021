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
    points, folds = inputFile.read().strip().split("\n\n")
    points = points.split("\n")
    folds = folds.split("\n")
    points = {Position(int(point.split(",")[0]), int(point.split(",")[1])) for point in points}
    folds = [fold.split()[2].split("=") for fold in folds]
    folds = [(a, int(b)) for [a, b] in folds]

def fold(points, fold):
    [direction, coord] = fold
    if direction == "y":
        return {p for p in points if p.y <= coord} | {Position(p.x, 2 * coord - p.y) for p in points if p.y > coord}
    if direction == "x":
        return {p for p in points if p.x <= coord} | {Position(2 * coord - p.x, p.y) for p in points if p.x > coord}
    raise("Unknown direction")

points = fold(points, folds[0])

result = len(points)



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
