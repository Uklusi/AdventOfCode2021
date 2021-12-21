from types import new_class
from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = True
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

distribution = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

turn = 0

state = (score1 + score2, start1, start2, score1, score2, turn)

numStates = defaultdict(int)
nextState = PriorityQueue()

numStates[state] = 1
nextState.put(state)
win1 = 0
win2 = 0
MAXSCORE = 21

while not nextState.empty():
    state = nextState.get()
    n = numStates[state]
    numStates[state] = 0
    s, p1, p2, score1, score2, turn = state
    # printLog(f"s: {s}, p1: {p1}, p2: {p2}, score1: {score1}, score2: {score2}, turn: {turn}")
    for (k, p) in distribution.items():
        flag = False
        if turn == 0:
            newp1 = (p1 + k) % 10
            newscore1 = score1 + (newp1 if newp1 else 10)
            s = newscore1 + score2
            if newscore1 >= MAXSCORE:
                win1 += n * p
                flag = True
            newState = (s, newp1, p2, newscore1, score2, 1)
        else:
            newp2 = (p2 + k) % 10
            newscore2 = score2 + (newp2 if newp2 else 10)
            s = score1 + newscore2
            if newscore2 >= MAXSCORE:
                win2 += n * p
                flag = True
            newState = (s, p1, newp2, score1, newscore2, 0)
        if not flag:
            if newState not in numStates:
                nextState.put(newState)
            numStates[newState] += n * p

result = max(win1, win2)




with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
