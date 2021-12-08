from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

decoding = []
output = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        currentDecoding = defaultdict(list)
        line = line.strip()
        dec, out = line.split(" | ")
        for s in dec.split():
            currentDecoding[len(s)].append(list(s))
        decoding.append(currentDecoding)
        output.append([set(x) for x in out.split()])

for out in output:
    for s in out:
        if len(s) in [2, 3, 4, 7]:
            result += 1







with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
