from itertools import starmap
from AoCUtils import *

result = 0
partNumber = "2"

writeToLog = False
if writeToLog:
    logFile = open("log" + partNumber + ".txt", "w")
else:
    logFile = "stdout"
printLog = printLogFactory(logFile)


# Type aliases, otherwise I'll go crazy
Pos = tuple[int, int, int]
Rot = int
BeacInd = int
ScanInd = int
Beacon = Pos
BeaconDiff = frozenset[Pos]

scanners: list[list[Beacon]] = []
scannersPos: list[Pos] = []

with open("input.txt", "r") as inputFile:
    lines = inputFile.read().strip().split("\n\n")
    for currentScanner in lines:
        currentScanner = currentScanner.split("\n")
        scannersPos.append((0, 0, 0))
        scanners.append([])
        for beacon in currentScanner[1:]:
            scanners[-1].append(tuple(int(n) for n in beacon.split(",")))

# I could have worked with PositionNDim, but I didn't so here we are
def diff(p1: Beacon, p2: Beacon) -> Pos:
    return tuple(p1[i] - p2[i] for i in range(len(p1)))

def add(p1: Pos, p2: Pos) -> Pos:
    return tuple(p1[i] + p2[i] for i in range(len(p1)))


def reorient(t: Pos, n: Rot) -> Pos:
    """
    Reorient takes a 3d position as tuple and a rotation index.
    All rotations of a coordinate system fixing the axis can be written as
    t^c * s^b * r^a, where a is 0 to 3, b is 0 or 1 and c is 0 to 2
    r is a 90 degree rotation around the x axis
    s is a 180 degree rotation around the z axis
    t is a 120 degree rotation around the line x = y = z (swapping the axis)
    We conventionally assign to each number 0 to 23 a unique rotation.
    """
    for _ in range(n % 4):
        t = (t[0], t[2], -t[1])
    if n // 12:
        t = (-t[0], -t[1], t[2])
    for _ in range((n // 4) % 3):
        t = (t[2], t[0], t[1])
    return t

def normalize(d: Pos) -> BeaconDiff:
    """
    Normalize returns the frozen set of all rotations of a 3d position
    At the beginning it was tuple(sorted(map(abs, d))),
    but this is not necessarily a result of a rotation (e.g. (-1, 2, 3) -> (1, 2, 3)).
    As it is defined, we have p1 in normalize(p2) iff normalize(p1) == normalize(p2)
    iff there exists n in 0 to 23 such that p1 == reorient(p2, n)
    """
    return frozenset(reorient(d, n) for n in range(24))

# beaconDiffs contains, for each beacon of each scanner,
# the relative position of all beacons from that scanner
# wrt the beacon we are considering
beaconDiffs = [
    [
        [
            diff(o, b) for o in currScanner
        ] for b in currScanner
    ] for currScanner in scanners
]

# BeaconDiffsNormalized is the same, but instead of an ordered list of differences,
# we consider the set of normalized differences
beaconDiffsNormalized = [
    [
        {
            normalize(relativePosition) for relativePosition in currBeaconDiff
        } for currBeaconDiff in currScanner
    ] for currScanner in beaconDiffs
]

def areScannersOverlapping(s1: ScanInd, s2: ScanInd) -> tuple[bool, BeacInd, BeacInd]:
    """
    Check if two scanners are overlapping (have 12 or more beacons in common,
    aka have the same relative position)
    If so, return a beacon from the first scanner and the corresponding one
    from the second scanner
    """
    k = [
        (len(d1 & d2) >= 12, i1, i2)
        for (i1, d1) in enumerate(beaconDiffsNormalized[s1])
        for (i2, d2) in enumerate(beaconDiffsNormalized[s2])
    ]
    k1 = list(map(lambda x: x[0], k))

    if any(k1):
        return k[k1.index(True)]
    else:
        return (False, -1, -1)

# connections has, for each scanner, the info about one overlapping scanner.
# This is done such that starting from 0 we can reach all other scanners.
# if scanners i and j overlap, and a beacon a from scanner i is the same as beacon b from scanner j,
# and rotation(b, rot) + offset == a, then we have that
# connection[j] = (i, rot, offset)
# As a consequence, at the end connection.keys() will be all the scanner indices
connections: dict[ScanInd, tuple[ScanInd, Rot, Pos]] = {0: (0, 0, (0, 0, 0))}
# Checked is a set of scanners for which we already checked for overlapping scanners
checked: set[ScanInd] = set()

while len(connections) < len(scanners):
    s1 = (set(connections.keys()) - checked).pop()
    s1: ScanInd

    for s2 in set(range(len(scanners))) - set(connections.keys()):
        s2: ScanInd

        overlap, b1, b2 = areScannersOverlapping(s1, s2)
        if not overlap:
            continue

        scanner1 = scanners[s1]
        scanner2 = scanners[s2]
        overlapping: list[tuple[BeacInd, BeacInd]] = []

        for (i, d1) in enumerate(beaconDiffs[s1][b1]):
            nd1 = normalize(d1)
            if nd1 in beaconDiffsNormalized[s2][b2]:
                for (j, d2) in enumerate(beaconDiffs[s2][b2]):
                    if nd1 == normalize(d2):
                        overlapping.append((i, j))

        # Coords will contain the coordinates of beacons in common between the two scanners,
        # as (c1, c2) where c1 is the coordinate for the first scanner and c2 for the second
        coords = [(scanner1[i], scanner2[j]) for (i, j) in overlapping]
        assert len(coords) >= 12
        # print(prettify(coords))

        d1 = diff(coords[0][0], coords[0][0]) # Avoid pylint unbound

        # Trying to find a difference vector that has 3 distinct components:
        # In this case we can get the unique rotation needed to make them coincide.
        # If there aren't, we should retry with a different first beacon,
        # but rn I just check it with an assert
        for ind in range(1, len(coords)):
            d1 = diff(coords[0][0], coords[ind][0])
            d2 = diff(coords[0][1], coords[ind][1])
            if len(normalize(d1)) == 24:
                break
        assert len(normalize(d1)) == 24

        for i in range(24):
            i: Rot
            if d1 == reorient(d2, i):
                orient: Rot = i
                # Now that the two beacons have the same axis directions,
                # We just need to find the offset between them
                offset = diff(coords[0][0], reorient(coords[0][1], orient))
                break
        # Safety assert: we want to check that the rotation and offset are indeed correct
        # We do that by checking that after the transformation the coordinates are all the same
        assert [p[0] for p in coords] == [add(reorient(p[1], orient), offset) for p in coords]

        connections[s2] = (s1, orient, offset)

    checked.add(s1)

# We assume that scanner 0 is in (0, 0, 0).
# Also each scanner has a starting position of (0, 0, 0) relative to itself
# For each other scanner, we check the scanner overlapping with it,
# and move the first scanner's position to the second scanner's coordinate system.
# Then, if the second scanner isn't 0, we repeat the process.
# Connections is constructed in such a way that we always reach 0.
for origconn in connections:
    conn = origconn
    scannerPos = scannersPos[conn]
    while conn != 0:
        (dest, rot, offset) = connections[conn]
        scannerPos = add(reorient(scannerPos, rot), offset)
        conn = dest
    scannersPos[origconn] = scannerPos

def manhattan(p1: Pos, p2: Pos) -> int:
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))

result = max(starmap(manhattan, product(scannersPos, repeat=2)))




with open("output" + partNumber + ".txt", "w") as outputFile:
    outputFile.write(str(result))
    print(str(result))

if writeToLog:
    cast(TextIOWrapper, logFile).close()
