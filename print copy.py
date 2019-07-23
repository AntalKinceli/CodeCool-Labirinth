import time
import math
P = "X"  # player mark
E = "O"  # endpoint mark
Px = 9  # + 1 the reall cordinate
Py = 2  # + 1 the reall cordinate
Ex = 14  # + 1 the reall cordinate
Ey = 5  # + 1 the reall cordinate
EDGE = 1 # map edge length
#LENGTH, WIDTH = 16, 80
def readfile(x): #("") reads your x file
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
def PLAYER():
    MAP[Py][Px] = P
def END():
    MAP[Ey][Ex] = E
def MOVE(x):
    direction = ""
    global Py, Px, EDGE
    x[Py][Px] = "."
    while direction not in ("w", "a", "s", "d"):
        direction = input("Give me WASD:")
        if direction == "quit":
            break
        continue
    if direction == "w" and Py - 1 - EDGE >= 0:
        Py -= 1      
    elif direction == "s" and len(x) > Py + 1 + EDGE:
        Py += 1
    elif direction == "a" and Px - 1 - EDGE >= 0:
        Px -= 1
    elif direction == "d" and len(x[0]) > Px + 1 + EDGE:
        Px += 1
    else:
        printout(suprise)
        time.sleep(2)



MAP = readfile("blank_map_edge.txt")  # calls readfile() to load your file content into a list
suprise = readfile("suprise.txt")
while True:
    PLAYER()
    END()
    if len(suprise) > len(MAP):
        print("-" * len(MAP[0]))
        for i in range(math.ceil(((len(suprise) - len(MAP)  + 1) / 2))):
            print()
        printout(MAP)
        for i in range(math.ceil(((len(suprise) - len(MAP)  + 1) / 2))):
            print()
        print("-" * len(MAP[0]))
    else:
        printout(MAP)
    MOVE(MAP)
