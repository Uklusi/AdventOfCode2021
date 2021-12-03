from AoCUtils import *
from collections import defaultdict

result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

freqs = {"0": 0, "1": 0}
nums = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        nums.append(line)
        freqs[line[0]] += 1
maxFreq = "0" if freqs["0"] > freqs["1"] else "1"
minFreq = "0" if freqs["0"] <= freqs["1"] else "1"

numsOxygen = [num for num in nums if num[0] == maxFreq]
numsCO2 = [num for num in nums if num[0] == minFreq]
oxygen = ""
co2 = ""

i = 1
while len(numsOxygen) > 1:
    freqs = {"0": 0, "1": 0}
    for num in numsOxygen:
        freqs[num[i]] += 1
    maxFreq = "0" if freqs["0"] > freqs["1"] else "1"
    numsOxygen = [num for num in numsOxygen if num[i] == maxFreq]
    i += 1

i = 1
while len(numsCO2) > 1:
    freqs = {"0": 0, "1": 0}
    for num in numsCO2:
        freqs[num[i]] += 1
    minFreq = "0" if freqs["0"] <= freqs["1"] else "1"
    numsCO2 = [num for num in numsCO2 if num[i] == minFreq]
    i += 1

result = int(numsOxygen[0], 2) * int(numsCO2[0], 2)






with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()

