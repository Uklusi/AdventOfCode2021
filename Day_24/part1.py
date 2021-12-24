from AoCUtils import *

writeToLog = False
writeToLog = True

useExample = False
# useExample = True


result = 0
partNumber = "1"

if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)

timer_start(partNumber)
instructions = []

n1List = []
n2List = []
flagList = []


inputFileName = ("example.txt" if useExample else "input.txt")
with open(inputFileName, "r") as inputFile:
    lines = inputFile.read().strip().split("\n")
    n = -1
    getN1 = False
    getN2 = False
    for line in lines:
        line = line.strip().split()
        if line[0] == "inp":
            n += 1
            ins = f"\ninput {line[1]}{n}"
        else:
            a = line[1]
            b = line[2]
            if b == "w":
                b = f"w{n}"

            match line[0]:

                case "add":
                    ins = f"{a} = {a} + {b}"
                    if getN1:
                        n1List.append(int(b))
                        getN1 = False
                    elif "w" in b:
                        getN2 = True
                    elif getN2:
                        n2List.append(int(b))
                        getN2 = False
                case "mul":
                    ins = f"{a} = {a} * {b}"
                case "div":
                    ins = f"{a} = {a} // {b}"
                    flagList.append(int(b) == 26)
                    getN1 = True
                case "mod":
                    ins = f"{a} = {a} mod {b}"
                case "eql":
                    ins = f"{a} = {a} == {b}"
                case _:
                    pass

        instructions.append(ins)

instr = "\n".join(instructions)
instr = re.sub(
    r"([xyz]) = \1 \* 0\n\1 = \1 \+ ([^\n]*)",
    lambda m: f"{m.group(1)} = {m.group(2)}",
    instr
)
instr = re.sub(
    r"([xyz]) = \1 == ([^\n]*)\n\1 = \1 == 0",
    lambda m: f"{m.group(1)} = {m.group(1)} != {m.group(2)}",
    instr
)
instr = re.sub(
    r"\n([^\n]*//[^\n]*)\n([^\n]*\n[^\n]*)\n",
    lambda m: f"\n{m.group(2)}\n{m.group(1)}\n",
    instr
)
instr = re.sub(
    "\n([xyz]) = ([^ \n]*)\n\1 = \1",
    lambda m: f"\n{m.group(1)} = {m.group(2)}",
    instr
)

printLog(instr.strip())

# print(n1List)
# print(n2List)
# print(flagList)

def step(z, w, n1, n2, flag):
    x = (z % 26) + n1
    if flag:
        z = z // 26
    if x != w:
        z = 26 * z + w + n2
    return z

def tryAllW(z, round):
    ret = []
    for w in range(1, 10):
        n1 = n1List[round]
        n2 = n2List[round]
        flag = flagList[round]
        ret.append(step(z, w, n1, n2, flag))
    return ret


coupled = []
coupledMachine = []
remaining = []
for (i, flag) in enumerate(flagList):
    if flag:
        (n2, j) = remaining.pop()
        coupledMachine.append((n2 + n1List[i], j, i))
        coupled.append((f"{n2 + n1List[i]} + w{j} = w{i}"))
    else:
        remaining.append((n2List[i], i))

print(coupled)

digits = [0 for _ in range(14)]

for (n, i, j) in coupledMachine:
    if n > 0:
        digits[j] = 9
        digits[i] = 9 - n
    else:
        digits[i] = 9
        digits[j] = 9 + n

result = join(digits)






timer_stop(partNumber)

with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
