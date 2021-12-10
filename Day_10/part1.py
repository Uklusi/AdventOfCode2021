from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

codeLines = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        codeLines.append(line)

CLOSED = [")", "]", "}", ">"]

def recursive(codeLine, n):
    if codeLine[n] in CLOSED:
        return (True, n, codeLine[n])
    else:
        before = codeLine[n]
    while n + 1 < len(codeLine) and codeLine[n + 1] not in CLOSED:
        n += 1
        (stop, n, reason) = recursive(codeLine, n)
        if stop:
            return (True, n, reason)
    n = n + 1
    if n >= len(codeLine):
        return (True, n, " ")
    match (before, codeLine[n]):
        case ("(", ")") | ("[", "]") | ("{", "}") | ("<", ">"):
            return (False, n, " ")
        case _:
            return (True, n, codeLine[n])

points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
    " ": 0
}

for codeLine in codeLines:
    (_, _, reason) = recursive(codeLine, 0)
    result += points[reason]



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
