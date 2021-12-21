from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)


start1 = 8
start2 = 9

# Example
# start1 = 4
# start2 = 8

score1 = 0
score2 = 0

turn = 0
movement = 6
while score1 < 1000 and score2 < 1000:
    if not turn % 2:
        start1 = (start1 + movement) % 10
        score1 = score1 + (start1 if start1 else 10)
    else:
        start2 = (start2 + movement) % 10
        score2 = score2 + (start2 if start2 else 10)
    movement = (movement - 1) % 10
    turn = turn + 1

result = min(score1, score2) * turn * 3

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
