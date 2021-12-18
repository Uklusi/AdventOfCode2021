from functools import reduce
from math import ceil
from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

nums = []

def parseLine(line):
    level = 0
    head = LinkedList(None, circular=False)
    current = head
    for c in line:
        match c:
            case "[":
                level += 1
            case "]":
                level += -1
            case "," | "\n":
                pass
            case _:
                current = current.add({"level": level, "value": int(c)})

    head = head.delete()
    return head

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        nums.append(parseLine(line.strip()))

def concat(l1, l2):
    a = l1
    a.data["level"] += 1
    while a.next is not None:
        a = a.next
        a.data["level"] += 1
    a.next = l2
    b = l2
    b.data["level"] += 1
    b.prev = a
    while b.next is not None:
        b = b.next
        b.data["level"] += 1
    return l1

def checkReduction(l1):
    a = l1
    explode = None
    split = None
    while a is not None:
        if explode is None and a.data["level"] == 5:
            explode = a
            break
        if split is None and a.data["value"] > 9:
            split = a
        a = a.next
    return (explode or split)

def explode(node):
    a = node
    b = node.next
    if a.prev is not None:
        a.prev.data["value"] += a.data["value"]
    if b.next is not None:
        b.next.data["value"] += b.data["value"]
    b.delete()
    a.data["level"] += -1
    a.data["value"] = 0
    return a

def split(node):
    a = node
    a.add({"level": a.data["level"] + 1, "value": ceil(a.data["value"] / 2)})
    a.data["level"] += 1
    a.data["value"] = a.data["value"] // 2
    return a

def printList(node):
    # not correct, but almost
    a = node
    chars = []
    levels = defaultdict(int)
    prevLev = 0
    while a is not None:
        lev = a.data["level"]
        levels[lev] += 1
        val = a.data["value"]

        if lev > prevLev:
            chars.extend(["["] * (lev - prevLev))
        chars.append(str(val))
        while levels[lev] == 2:
            levels[lev] = 0
            chars.append("]")
            lev += -1
            levels[lev] += 1
        chars.append(",")
        prevLev = lev
        a = a.next
    return join(chars[:-1])

def sumList(l1, l2):
    node = concat(l1, l2)
    # printLog(printList(node))
    reduction = checkReduction(node)
    while reduction is not None:
        newstart = node
        if reduction.data["level"] == 5:
            _ = explode(reduction)
            if node.prev is not None:
                node = node.prev
            newstart = node
        else:
            newstart = split(reduction)
        reduction = checkReduction(newstart)
        # printLog(printList(node))
    return node

def calcMagnitude(origNode, level=1):
    node = origNode
    ret = 0
    if node.data["level"] == level:
        ret += 3 * int(node.data["value"])
    else:
        (node, n) = calcMagnitude(node, level + 1)
        ret += 3 * n
    node = node.next
    if node.data["level"] == level:
        ret += 2 * int(node.data["value"])
    else:
        (node, n) = calcMagnitude(node, level + 1)
        ret += 2 * n
    return (node, ret)



result = max(map(
    lambda l: calcMagnitude(sumList(*l))[1],
    [(deepcopy(a), deepcopy(b)) for (a, b) in product(nums, repeat=2) if a != b]
))


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
