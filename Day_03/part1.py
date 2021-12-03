from AoCUtils import *
from collections import defaultdict

result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

freqs = defaultdict(lambda: {"0": 0, "1": 0})

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        for (i, c) in enumerate(line):
            freqs[i][c] += 1

gamma = ""
epsilon = ""

for i in range(len(freqs)):
    if freqs[i]["0"] > freqs[i]["1"]:
        gamma += "0"
    else:
        gamma += "1"
    if freqs[i]["0"] < freqs[i]["1"]:
        epsilon += "0"
    else:
        epsilon += "1"
        
result = int(gamma, 2) * int(epsilon, 2)






with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()

