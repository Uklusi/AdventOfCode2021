from AoCUtils import *


result = 0
partNumber = "2"

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

def traverse(prevSmall, prevPath, doubleSmall, current):
    # printLog(current)
    if current == "end":
        # printLog(prevPath)
        global result
        result += 1
        return
    for next in paths[current]:
        currPath = prevPath + [next]
        currSmall = prevSmall.copy()
        currDoubleSmall = doubleSmall
        if next.islower():
            if next not in prevSmall:
                currSmall |= {next}
            elif not doubleSmall and next not in ["start", "end"]:
                currDoubleSmall = True
            else:
                # printLog(currPath)
                # printLog(currSmall)
                continue
        traverse(currSmall, currPath, currDoubleSmall, next)
    return


traverse({"start"}, ["start"], False, "start")





with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
