from AoCUtils import *


result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

insertionRules = {}

with open("input.txt", "r") as inputFile:
    (input, lines) = inputFile.read().strip().split("\n\n")
    lines = lines.split("\n")
    for line in lines:
        line = line.strip().split(" -> ")
        insertionRules[line[0]] = line[1]

transformationRules = {}

for s in insertionRules.keys():
    ins = insertionRules[s]
    transformationRules[s] = [s[0] + ins, ins + s[1]]

pairsCount = defaultdict(int)

for pair in zip(input, input[1:]):
    pair = join(pair)
    pairsCount[pair] += 1

for _ in range(40):
    newPairsCount = defaultdict(int)
    for (pair, n) in pairsCount.items():
        trans = transformationRules[pair]
        newPairsCount[trans[0]] += n
        newPairsCount[trans[1]] += n
    pairsCount = newPairsCount

countLetters = {
    let: (
        sum(n * pair.count(let) for (pair, n) in pairsCount.items()) +
        join([input[0], input[-1]]).count(let)
    ) // 2
    for let in set(insertionRules.values())
}

result = max(countLetters.values()) - min(countLetters.values())


with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
