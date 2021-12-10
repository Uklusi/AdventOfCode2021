from AoCUtils import *


result = 0
partNumber = "2"

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
MATCHING = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}
POINTS = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

def recursive(codeLine, n):
    score = 0
    if codeLine[n] in CLOSED:
        return (True, n, -1)
    else:
        before = codeLine[n]
    while n + 1 < len(codeLine) and codeLine[n + 1] not in CLOSED:
        n += 1
        (stop, n, score) = recursive(codeLine, n)
        if stop:
            return (True, n, score)
    n = n + 1
    if n >= len(codeLine):
        return (False, n, score * 5 + POINTS[before])
    match (before, codeLine[n]):
        case ("(", ")") | ("[", "]") | ("{", "}") | ("<", ">"):
            return (False, n, 0)
        case _:
            return (True, n, -1)

incomplete = [ret for (mismatch, _, ret) in [recursive(codeLine, 0) for codeLine in codeLines] if not mismatch]
incomplete.sort()

result = incomplete[len(incomplete) // 2]




with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
