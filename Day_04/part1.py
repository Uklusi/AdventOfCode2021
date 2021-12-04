from AoCUtils import *
import numpy as np

result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

drawList: list[int] = []
boardList: list[np.ndarray] = []
# boardDictList: list[dict[str, dict[int, dict[int, int]]]] = []
boardNumsList: list[dict[int, tuple[int, int]]] = []
with open("input.txt", "r") as inputFile:
    sections = inputFile.read().strip().split("\n\n")
    drawList = [int(n) for n in sections.pop(0).split(",")]
    for s in sections:
        boardList.append(np.array([[int(n) for n in r.split()] for r in s.split("\n")]))
        # boardDictList.append({"r": {i: {} for i in range(5)}, "c": {i: {} for i in range(5)}})
        boardNumsList.append({})
        for (i, j) in product(range(5), range(5)):
            # boardDictList[-1]["r"][i][j] = boardList[-1][i][j]
            # boardDictList[-1]["c"][j][i] = boardList[-1][i][j]
            boardNumsList[-1][boardList[-1][i, j]] = (i, j)

boardExtractedList: list[np.ndarray] = [np.array([[False for _ in range(5)] for _ in range(5)]) for _ in range(len(boardList))]

def checkWin(boards: list[np.ndarray]) -> tuple[bool, int]:
    for (n, b) in enumerate(boards):
        ret = False
        ret |= any([b[:, i].all() for i in range(5)])
        ret |= any([b[i, :].all() for i in range(5)])
        if ret:
            return (True, n)
    return (False, -1)

for draw in drawList:
    for (n, board) in enumerate(boardNumsList):
        if draw in board:
            boardExtractedList[n][boardNumsList[n][draw]] = True
    (win, boardNum) = checkWin(boardExtractedList)
    if win:
        break

board = boardList[boardNum]
boardExtracted = boardExtractedList[boardNum]
result = sum([board[i, j] for (i, j) in product(range(5), range(5)) if not boardExtracted[i, j]])

result *= draw


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()

