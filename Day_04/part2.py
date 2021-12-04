from AoCUtils import *
import numpy as np

result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

drawList: list[int] = []
boardList: list[np.ndarray] = []
boardNumsList: list[dict[int, tuple[int, int]]] = []
with open("input.txt", "r") as inputFile:
    sections = inputFile.read().strip().split("\n\n")
    drawList = [int(n) for n in sections.pop(0).split(",")]
    for s in sections:
        boardList.append(np.array([[int(n) for n in r.split()] for r in s.split("\n")]))
        boardNumsList.append({})
        for (i, j) in product(range(5), range(5)):
            boardNumsList[-1][boardList[-1][i, j]] = (i, j)

boardExtractedList: list[np.ndarray] = [np.array([[False for _ in range(5)] for _ in range(5)]) for _ in range(len(boardList))]

def checkWin(boards: list[np.ndarray], prevWinning: list[int]) -> list[int]:
    winning = prevWinning.copy()
    for (n, b) in enumerate(boards):
        if n not in winning:
            win = False
            win |= any([b[:, i].all() for i in range(5)])
            win |= any([b[i, :].all() for i in range(5)])
            if win:
                winning.append(n)
    return winning

winning = []
for draw in drawList:
    for (n, board) in enumerate(boardNumsList):
        if draw in board:
            boardExtractedList[n][boardNumsList[n][draw]] = True
    winning = checkWin(boardExtractedList, prevWinning=winning)
    if len(winning) == len(boardList):
        break

board = boardList[winning[-1]]
boardExtracted = boardExtractedList[winning[-1]]
result = sum([board[i, j] for (i, j) in product(range(5), range(5)) if not boardExtracted[i, j]])

result *= draw


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()

