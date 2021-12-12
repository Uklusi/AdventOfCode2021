from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

paths = defaultdict(set)

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        (a, b) = line.split("-")
        paths[a].add(b)
        paths[b].add(a)

def traverse(prevSmall, prev, current):
    if current == "end":
        # printLog(prev)
        global result
        result += 1
        return
    for next in paths[current] - prevSmall:
        if next.islower():
            traverse(prevSmall | {next}, prev + [next], next)
        else:
            traverse(prevSmall, prev + [next], next)
    return


traverse({"start"}, ["start"], "start")





with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
