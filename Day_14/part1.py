from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

insertionRules = {}

with open("input.txt", "r") as inputFile:
    (input, lines) = inputFile.read().strip().split("\n\n")
    lines = lines.split("\n")
    for line in lines:
        line = line.strip().split(" -> ")
        insertionRules[line[0]] = line[1]

for _ in range(10):
    pairs = zip(input, input[1:])
    newInput = [input[0]]
    for p in pairs:
        key = p[0] + p[1]
        newInput.extend([insertionRules[key], p[1]])
    input = newInput

letters = set(input)
frequencies = {l: sum(1 for c in input if c == l) for l in letters}
result = max(frequencies.values()) - min(frequencies.values())

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
