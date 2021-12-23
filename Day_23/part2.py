from numpy import ndarray
from AoCUtils import *

writeToLog = False
# writeToLog = True

useExample = False
# useExample = True


result = 0
partNumber = "2"

if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

timer_start(partNumber)

class hashableArray():
    def __init__(self, array: ndarray):
        self.array = array

    def __hash__(self):
        return hash(tuple(self.array.flatten()))

    def __eq__(self, other):
        return np.array_equal(self.array, other.array)

burrowList: list[list[str]] = []

addToInput = [list("###D#C#B#A###"), list("###D#B#A#C###")]

inputFileName = ("example.txt" if useExample else "input.txt")
with open(inputFileName, "r") as inputFile:
    lines = inputFile.read().split("\n")
    n = len(lines[0])
    for line in lines:
        line = line.replace(" ", "#").ljust(n, "#")
        burrowList.append(list(line))
burrowList = burrowList[:-2] + addToInput + burrowList[-2:]

burrow = hashableArray(np.array(burrowList).transpose())

letterToRoomX = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9
}
roomXToLetter = {v: k for (k, v) in letterToRoomX.items()}

letterToCost = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

maxY = len(burrowList) - 2

corridorPositions = frozenset([
    (1, 1),
    (2, 1),
    (4, 1),
    (6, 1),
    (8, 1),
    (10, 1),
    (11, 1)
])
roomPositions = frozenset((a, b) for a in letterToRoomX.values() for b in range(2, maxY + 1))

possiblePositions = corridorPositions | roomPositions

Pos = tuple[int, int]

@cache
def shouldMove(burrow: hashableArray, start: Pos) -> bool:
    """
    Check if the amphipod should move, i.e.
    it's in the corridor
    or it is in the wrong side room
    or it is blocking a pod in the wrong room
    """
    if start in corridorPositions:
        return True
    let = roomXToLetter[start[0]]
    return not all(burrow.array[(start[0], b)] == let for b in range(start[1], maxY + 1))

@cache
def isSideRoomOk(burrow: hashableArray, target: MapPosition, type: str) -> bool:
    """
    Check if the pod can move in the room, i.e.
    it is the correct room,
    the room has not a wrong pod,
    and the pod is moving in the last space available
    """
    if target.x != letterToRoomX[type]:
        return False
    n = maxY
    while n != target.y:
        if burrow.array[(target.x, n)] != type:
            return False
        n += -1
    return True

@cache
def isMoveAcceptable(burrow: hashableArray, start: MapPosition, end: MapPosition) -> bool:
    """
    Check for the following conditions:
    - the end position is not in front of a room
    - the pod is not already in place
    - the pod is moving from a room to a corridor OR
    - the pod is moving from a corridor to its correct room, in the last space available
    """
    startc = start.stdcoords()
    endc = end.stdcoords()
    if endc not in possiblePositions:
        return False
    if not shouldMove(burrow, startc):
        return False
    if startc in corridorPositions:
        if endc in corridorPositions:
            return False
        return isSideRoomOk(burrow, end, burrow.array[start.stdcoords()])
    else:
        return endc in corridorPositions

posList = frozenset((a, b) for a in letterToRoomX.values() for b in range(2, maxY + 1))

@cache
def checkVictory(burrow: hashableArray) -> bool:
    return all(burrow.array[(a, b)] == k for (k, a) in letterToRoomX.items() for b in range(2, maxY + 1))

@cache
def getOptimalMove(burrow: hashableArray, letter: str) -> Optional[Pos]:
    roomX = letterToRoomX[letter]
    if all(burrow.array[(roomX, b)] in (letter, ".") for b in range(2, maxY + 1)):
        return (roomX, max(i for i in range(2, maxY + 1) if burrow.array[(roomX, i)] == "."))
    return None

@cache
def occupied(frame: hashableArray, pos: MapPosition) -> bool:
    return frame.array[pos.stdcoords()] != "."

# Solution by hand
minVal = 46771

@cache
def triang(n):
    return n * (n + 1) // 2

@cache
def minPossibleScore(burrow: hashableArray, posList: frozenset[Pos], currentScore: int) -> int:
    ret = currentScore
    needMoving = {let: 0 for let in "ABCD"}
    for start in posList:
        posStart = Position(*start)
        letter = burrow.array[start]
        if letter == roomXToLetter.get(posStart.x, "X"):
            continue
        needMoving[letter] += 1
        ret += (letterToCost[letter] * posStart.distance(Position(letterToRoomX[letter], 1)))
    for letter in needMoving:
        ret += (triang(needMoving[letter]) * letterToCost[letter])
    return ret

@cache
def executeMove(
    burrow: hashableArray, start: MapPosition, end: MapPosition, posList: frozenset[Pos]
) -> tuple[hashableArray, frozenset[Pos], int]:

    newBurrow = deepcopy(burrow)
    startc = start.stdcoords()
    endc = end.stdcoords()
    middle = Position(start.x, 1)
    newPosList = (posList | {endc}) - {startc}
    cost = letterToCost[burrow.array[startc]] * (start.distance(middle) + middle.distance(end))
    (newBurrow.array[startc], newBurrow.array[endc]) = (".", newBurrow.array[startc])
    return (newBurrow, newPosList, cost)


@cache
def step(burrow: hashableArray, score: int, posList: frozenset[Pos]) -> int:
    # printLog(Image(burrow.array.transpose()))
    # printLog(f"Score: {score}")
    # printLog()
    global minVal
    bestScore = minPossibleScore(burrow, posList, score)
    if bestScore >= minVal:
        # printLog(f"killing for excessive score: current {score}, min {bestScore}")
        # printLog("----------------")
        # printLog()
        return inf
    if checkVictory(burrow):
        minVal = score
        # printLog(f"victory with score {score}")
        # printLog("----------------")
        # printLog()
        return score
    s = inf
    newMove = True
    while newMove:
        newMove = False
        possibleEnds: dict[Pos, dict[MapPosition, int]] = {}
        for startc in posList:
            # # printLog(f"start: {start}")
            mapStart = MapPosition(*startc, frame=burrowList, occupied=partial(occupied, burrow), reverseY=False)
            if not shouldMove(burrow, startc):
                continue
            possibleEnds[startc] = dijkstra(mapStart)

        for startc in posList:
            mapStart = MapPosition(*startc, frame=burrowList, occupied=partial(occupied, burrow), reverseY=False)
            if not shouldMove(burrow, startc):
                continue
            targetc = getOptimalMove(burrow, burrow.array[startc])
            if targetc is None:
                continue
            possibleEndsCoords = list(map(lambda p: p.stdcoords(), possibleEnds[startc].keys()))
            if targetc in possibleEndsCoords:
                target = MapPosition(*targetc, frame=burrowList, occupied=partial(occupied, burrow), reverseY=False)
                newMove = True
                (burrow, posList, cost) = executeMove(burrow, mapStart, target, posList)
                # printLog(f"{startc} -> {targetc}, cost {cost}")
                score += cost
                # printLog(Image(burrow.transpose()))
                # printLog(f"Score: {score}")
                # printLog()
                break

    if checkVictory(burrow):
        minVal = score
        # printLog(f"victory with score {score}")
        # printLog("----------------")
        # printLog()
        return score

    for startc in posList:
        mapStart = MapPosition(*startc, frame=burrowList, occupied=partial(occupied, burrow), reverseY=False)
        if not shouldMove(burrow, startc):
            continue
        if startc in corridorPositions:
            continue
        # printLog(f"start: {startc}")
        ends = dijkstra(mapStart)
        for end in ends:
            if end != mapStart:
                # printLog(f"considering target: {end.stdcoords()}")
                if isMoveAcceptable(burrow, mapStart, end):
                    (newBurrow, newPosList, cost) = executeMove(burrow, mapStart, end, posList)
                    # printLog()
                    # printLog("----------------")
                    # printLog(f"move accepted: {startc} -> {end.stdcoords()}, cost {cost}")
                    # printLog()
                    # printLog(Image(burrow.transpose()))
                    # printLog(f"Score: {score}")
                    # printLog()
                    s = min(s, step(newBurrow, score + cost, newPosList))
    # printLog(f"no more moves, returning with score {s}")
    # printLog("----------------")
    # printLog()
    return s

result = step(burrow, 0, posList)


timer_stop(partNumber)

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
