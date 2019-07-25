import time
import math
import sys
import os
import tty
import termios

P = "X"  # player mark
E = "O"  # endpoint mark
F = "Z"  # fog mark
px = 1  # + 1 the reall cordinate
py = 1  # + 1 the reall cordinate
endx = 1  # + 1 the reall cordinate
endy = 2  # + 1 the reall cordinate
EDGE = 1  # map edge length
WALL = ["|", "-"]  # wall marks
TRAIL = "."  # player trail mark
REVEAL = 1  # player reveal zone range


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readfile(x):  # ("") reads your x file
    with open(x) as f:
        y = f.read().splitlines()
        z = []
        f.close
        for i in y:  # makes list array from string
            z.append(list(i))
        return z


def blank_map(x, y, g):  # generates x width, y heigth list with full of g
    z = []
    for i in range(y):
        z.append([g] * x)
    return z


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def printout(x):
    for i in x:
        print("".join(i))


def main_print(x, y):
    cls()
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


def move(x, y, z, f):
    direction = ""
    while direction not in ("w", "a", "s", "d", "q"):
        direction = getch()
        continue
    if direction == "q":
        sys.exit()
    elif direction == "w" and z - 1 - EDGE >= 0 and x[z - 1][f] not in WALL:
        z -= 1
    elif direction == "s" and len(x) > z + 1 + EDGE and x[z + 1][f] not in WALL:
        z += 1
    elif direction == "a" and f - 1 - EDGE >= 0 and x[z][f - 1] not in WALL:
        f -= 1
    elif direction == "d" and len(x[0]) > f + 1 + EDGE and x[z][f + 1] not in WALL:
        f += 1
    else:
        cls()
        printout(surprise)
        time.sleep(1.5)
    return z, f


def checkwin(x):
    if py == endy and px == endx:
        cls()
        printout(x)
        time.sleep(2)
        cls()
        mainmenu()


# labyrinth_map = readfile("first_map.txt")  # to load your file content into a list
# load tutorial to a list / aternate w/ previous line

def mainmenu():
    global mapfog
    x = ""
    file = open("main_menu.txt", "r")
    cont = file.read()
    print(cont)
    file.close()
    mm = getch() #input()
    if mm == "0":
        x = readfile("tutorial_map.txt")
    elif mm == "1":
        x = readfile("first_map.txt")
    elif mm == "q":
        exit()
    return x
    mapfog = blank_map(len(labyrinth_map[0]), len(labyrinth_map), F)
    main_print(mapfog, surprise)




labyrinth_map = mainmenu()

surprise = readfile("surprise.txt")  # to load your file content into a list
win = readfile("win.txt")  # to load your file content into a list
# creating fog map with the same size as labyrinth
mapfog = blank_map(len(labyrinth_map[0]), len(labyrinth_map), F)
spaceing = math.ceil(((len(surprise) - len(labyrinth_map) + 1) / 2))

labyrinth_map[py][px] = P
labyrinth_map[endy][endx] = E
mapfog[py][px] = P
revealrange = range(-REVEAL, REVEAL + 1)


if EDGE > 0:  # reaveals map edge if it has any
    for i in range(EDGE):
        mapfog[0 + i] = labyrinth_map[0 + i]
        mapfog[-1 - i] = labyrinth_map[-1 - i]
        for z, x in enumerate(labyrinth_map):
            mapfog[z][0 + i] = labyrinth_map[z][0 + i]
            mapfog[z][-1 - i] = labyrinth_map[z][-1 - i]
for i in labyrinth_map:  # reaveals stuff around player
    for i in revealrange:
        for z in revealrange:
            mapfog[py + i][px + z] = labyrinth_map[py + i][px + z]


while True:  # main loop
    main_print(mapfog, surprise)
    checkwin(win)
    labyrinth_map[py][px] = TRAIL  # switches player mark to trail mark
    mapfog[py][px] = labyrinth_map[py][px]
    py, px = move(labyrinth_map, mapfog, py, px)
    labyrinth_map[py][px] = P  # update player position
    mapfog[py][px] = P  # update player position
    for i in revealrange:  # reaveal stuff around player
        for z in revealrange:
            mapfog[py + i][px + z] = labyrinth_map[py + i][px + z]
