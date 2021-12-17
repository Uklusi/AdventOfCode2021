from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = True
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)


with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()

"""target area: x=207..263, y=-115..-63"""

xmin = 207
xmax = 263
ymin = -115
ymax = -63

# Example values
# xmin = 20
# xmax = 30
# ymin = -10
# ymax = -5

# I wanted something smarter, I just lost a bunch of time
def triang(n):
    return n * (n + 1) // 2

def newStart(vx, vy):
    if vy < 0:
        return (0, 0, vx, vy)
    n = 2 * vy + 1
    k = max(0, vx - n)
    return (triang(vx) - triang(k), 0, k, -vy - 1)

def launch(x, y, ovx, ovy):
    # ovx, ovy are just for debugging, i could have used vx and vy directly
    # but then I would lose the input values and could not debug based on that
    (vx, vy) = (ovx, ovy)
    inTarget = (xmin <= x <= xmax) and (ymin <= y <= ymax)
    overshoot = (xmax < x) or (ymin > y)

    while (not inTarget) and (not overshoot):
        x = x + vx
        y = y + vy
        vy += -1
        vx = max(vx - 1, 0)
        inTarget = (xmin <= x <= xmax) and (ymin <= y <= ymax)
        overshoot = (xmax < x) or (ymin > y)

    if inTarget:
        return 1
    return 0

for vx, vy in product(range(xmax + 1), range(ymin, -ymin)):
    r = launch(*newStart(vx, vy))
    # r = launch(0, 0, vx, vy)
    result += r
    # if r:
    #     printLog(vx, vy)


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
