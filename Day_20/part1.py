from AoCUtils import *


result = 0
partNumber = "1"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)


with open("input.txt", "r") as inputFile:
    [enhancer, imageStr] = inputFile.read().strip().split("\n\n")
    enhancer = enhancer.replace(".", "0").replace("#", "1")
    imageStr = imageStr.replace(".", "0").replace("#", "1")
    image = imageStr.split("\n")

def b(c):
    if c == ".":
        return "0"
    return "1"

def adj(t: tuple[int, int]):
    return [(t[0] + i, t[1] + j) for j in range(-1, 2) for i in range(-1, 2)]

def getPixel(t: tuple[int, int], image: Sequence[Sequence[str]], out: str):
    if t[0] < 0 or t[0] >= len(image[0]) or t[1] < 0 or t[1] >= len(image):
        return out
    else:
        return image[t[1]][t[0]]


for counter in range(2):
    if counter % 2:
        # Assuming either (enhancer[0] = 0 and enhancer[-1] = 1) or (enhancer[0] = 1 and enhancer[-1] = 0)
        out = enhancer[0]
    else:
        out = "0"
    newImage = []
    for y in range(-1, len(image) + 1):
        newImage.append([])
        for x in range(-1, len(image[0]) + 1):
            nBin = ""
            for t in adj((x, y)):
                nBin += getPixel(t, image, out)
            n = int(nBin, 2)
            newImage[-1].append(enhancer[n])
    image = newImage


result = sum(map(lambda x: x.count("1"), image))



with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
