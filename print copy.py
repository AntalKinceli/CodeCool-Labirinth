import time
import math
import sys


P = "X"  # player mark
E = "O"  # endpoint mark
Px = 9  # + 1 the reall cordinate
Py = 2  # + 1 the reall cordinate
Ex = 14  # + 1 the reall cordinate
Ey = 5  # + 1 the reall cordinate
EDGE = 1  # map edge length
WALL = ["|", "-"]

def readfile(x):  # ("") reads your x file
    with open(x) as f:
        y = f.read().splitlines()
        z = []
        f.close
        for i in y:
            z.append(list(i))
        return z
def blank_map(x, y):
    z = []
    for i in range(y):
        z.append(["0"] * x)
    return z
def printout(x):
    for i in x:
        print("".join(i))
def MAINPRINT(x, y):
    global spaceing
    if len(y) > len(x):
        print("-" * len(x[0]))
        for i in range(spaceing):
            print()
        printout(x)
        for i in range(spaceing):
            print()
        print("-" * len(x[0]))
    else:
        printout(x)
def MOVE(x):
    direction = ""
    global Py, Px, EDGE
    x[Py][Px] = "."
    while direction not in ("w", "a", "s", "d", "quit"):
        direction = input("Give me WASD:")
        continue
    if direction == "quit":
        sys.exit()
    elif direction == "w" and Py - 1 - EDGE >= 0 and x[Py- 1][Px]  not in WALL:
        Py -= 1
    elif direction == "s" and len(x) > Py + 1 + EDGE and x[Py + 1][Px] not in WALL:
        Py += 1
    elif direction == "a" and Px - 1 - EDGE >= 0 and x[Py][Px - 1] not in WALL:
        Px -= 1
    elif direction == "d" and len(x[0]) > Px + 1 + EDGE and x[Py][Px + 1] not in WALL:
        Px += 1
    elif direction in ("w", "a", "s", "d"):
        printout(suprise)
        time.sleep(2)
    x[Ey][Ex] = E
    x[Py][Px] = P
def CHECKWIN(x):
    if Py == Ey and Px == Ex:
        printout(x)
        sys.exit()

MAP = readfile("first_map.txt")  # calls readfile() to load your file content into a list
suprise = readfile("suprise.txt")
win = readfile("win.txt")
spaceing = math.ceil(((len(suprise) - len(MAP) + 1) / 2))
MAP[Py][Px] = P
MAP[Ey][Ex] = E


while True:
    MAINPRINT(MAP, suprise)
    CHECKWIN(win)
    MOVE(MAP)
