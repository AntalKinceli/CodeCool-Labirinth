import time
import math
import sys
import os

P = "X"  # player mark
E = "O"  # endpoint mark
px = 9  # + 1 the reall cordinate
py = 2  # + 1 the reall cordinate
endx = 14  # + 1 the reall cordinate
endy = 5  # + 1 the reall cordinate
EDGE = 1  # map edge length
WALL = ["|", "-"]


def readfile(x):  # ("") reads your x file
    with open(x) as f:
        y = f.read().splitlines()
        z = []
        f.close
        for i in y:  # makes list array from string
            z.append(list(i))
        return z


def blank_map(x, y):  # not used any more
    z = []
    for i in range(y):
        z.append(["0"] * x)
    return z


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def printout(x):
    for i in x:
        print("".join(i))


def main_print(x, y):
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


def move(x):
    direction = ""
    global py, px
    x[py][px] = "."
    while direction not in ("w", "a", "s", "d", "quit"):
        direction = input("Give me WASD:")
        continue
    if direction == "quit":
        sys.exit()
    elif direction == "w" and py - 1 - EDGE >= 0 and x[py - 1][px] not in WALL:
        py -= 1
    elif direction == "s" and len(x) > py + 1 + EDGE and x[py + 1][px] not in WALL:
        py += 1
    elif direction == "a" and px - 1 - EDGE >= 0 and x[py][px - 1] not in WALL:
        px -= 1
    elif direction == "d" and len(x[0]) > px + 1 + EDGE and x[py][px + 1] not in WALL:
        px += 1
    else:
        printout(surprise)
        time.sleep(2)
    x[py][px] = P


def checkwin(x):
    if py == endy and px == endx:
        cls()
        printout(x)
        sys.exit()


# calls readfile() to load your file content into a list
labyrinth_map = readfile("first_map.txt")
surprise = readfile("surprise.txt")
win = readfile("win.txt")
spaceing = math.ceil(((len(surprise) - len(labyrinth_map) + 1) / 2))
labyrinth_map[py][px] = P
labyrinth_map[endy][endx] = E


while True:
    main_print(labyrinth_map, surprise)
    checkwin(win)
    move(labyrinth_map)
