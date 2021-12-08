from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

decoding = []
output = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        currentDecoding = defaultdict(list)
        line = line.strip()
        dec, out = line.split(" | ")
        for s in dec.split():
            currentDecoding[len(s)].append(set(s))
        decoding.append(currentDecoding)
        output.append([set(x) for x in out.split()])

defaultSegments = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg")
}

for (i, dec) in enumerate(decoding):
    out = output[i]

    seg1 = dec[2][0]
    seg3 = [x for x in dec[5] if x > seg1][0]
    seg4 = dec[4][0]
    seg7 = dec[3][0]
    seg8 = dec[7][0]

    segA = list(seg7 - seg1)[0]
    segG = list(seg3 - seg4 - seg7)[0]
    segB = list(seg4 - seg3)[0]
    segD = list(seg4 - seg1 - {segB})[0]

    seg5 = [x for x in dec[5] if segB in x][0]
    segF = list(seg5 & seg1)[0]
    segC = list(seg1 - {segF})[0]
    segE = list(seg8 - seg5 - {segC})[0]

    mapSegs = {
        "a": segA,
        "b": segB,
        "c": segC,
        "d": segD,
        "e": segE,
        "f": segF,
        "g": segG
    }

    mapNums = {frozenset(mapSegs[x] for x in segs): n for (n, segs) in defaultSegments.items()}
    decodedOutput = int(join([str(mapNums[frozenset(x)]) for x in out]))
    result += decodedOutput










with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
