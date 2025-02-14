import time
import math
import sys
import os
import tty
import termios


def getch():  # turtle
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
        h = []
        f.close
        for i in y:  # makes list array from string
            if i[:1] != "ß":
                z.append(list(i))
            else:
                j = i.lstrip(i[0])
                j = j[0:j.rfind("ß")]
                if j[:1] == "[":
                    j = j.strip("[]")
                    j = j.split(",")
                    for l, k in enumerate(j):
                        if k.isdigit() is True:
                            j[l] = (int(j[l]))
                elif j[:1].isdigit() is True:
                    j = int(j)
                h.append(j)
        return z, h


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
    h = False
    while direction not in ("w", "a", "s", "d", "q"):
        direction = getch()
        continue
    if direction == "q":
        h = True
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
        time.sleep(1)
    return z, f, h


def checkwin(x):
    if py == endy and px == endx:
        cls()
        printout(x)
        time.sleep(2)
        cls()
        return True


def mainmenu():
    cls()
    x = ""
    mm = ""
    file = open("main_menu.txt", "r")
    cont = file.read()
    print(cont)
    file.close()
    while mm not in ["0", "1", "2", "q"]:
        mm = getch()  # input()
    if mm == "0":
        x = "tutorial_map.txt"
    elif mm == "1":
        x = "first_map.txt"
    elif mm == "2":
        x = "second_map.txt"
    elif mm == "q":
        exit()
    return x


while True:
    labyrinth_map = mainmenu()
    # to load your file content into a list
    surprise, asd = readfile("surprise.txt")
    win, dsa = readfile("win.txt")  # to load your file content into a list
    # to load your file content into a list
    labyrinth_map, settings = readfile(labyrinth_map)
    (P,
     E,
     F,
     px,
     py,
     endx,
     endy,
     EDGE,
     WALL,
     TRAIL,
     REVEAL) = settings
    # to load your file variables into variables
    surprise, asd = readfile("surprise.txt")
    win, dsa = readfile("win.txt")  # to load your file content into a list
    # creating fog map with the same size as labyrinth
    mapfog = blank_map(len(labyrinth_map[0]), len(labyrinth_map), F)
    spaceing = math.ceil(((len(surprise) - len(labyrinth_map) + 1) / 2))

    labyrinth_map[py][px] = P
    labyrinth_map[endy][endx] = E
    mapfog[py][px] = P
    revealrange = range(-REVEAL, REVEAL + 1)  # -1, 0, 1

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
        if checkwin(win) and check_quit()
        break
        labyrinth_map[py][px] = TRAIL  # switches player mark to trail mark
        mapfog[py][px] = labyrinth_map[py][px]
        py, px = move(labyrinth_map, mapfog, py, px)

        labyrinth_map[py][px] = P  # update player position
        mapfog[py][px] = P  # update player position
        for i in revealrange:  # reaveal stuff around player
            for z in revealrange:
                mapfog[py + i][px + z] = labyrinth_map[py + i][px + z]
