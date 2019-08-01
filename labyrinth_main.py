import time
import math
import sys
import os
import tty
import termios


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


def move(fullmap, player_y, player_x):
    direction = ""
    h = False
    while direction not in ("w", "a", "s", "d", "q"):
        direction = getch()
        continue
    if direction == "q":
        h = True
    elif direction == "w" and fullmap[player_y - 1][player_x] not in WALL:
        player_y -= 1
    elif direction == "s" and fullmap[player_y + 1][player_x] not in WALL:
        player_y += 1
    elif direction == "a" and fullmap[player_y][player_x - 1] not in WALL:
        player_x -= 1
    elif direction == "d" and fullmap[player_y][player_x + 1] not in WALL:
        player_x += 1
    else:
        cls()
        printout(surprise)
        time.sleep(1)
    return player_y, player_x, h


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
    current_map = mainmenu()
    surprise, asd = readfile("surprise.txt")
    win, dsa = readfile("win.txt")  # to load your file content into a list
    # to load your file content into a list
    current_map, settings = readfile(current_map)
    (P,
     E,
     F,
     WALL,
     TRAIL,
     REVEAL) = settings
    # to load your file variables into variables
    surprise, asd = readfile("surprise.txt")
    win, dsa = readfile("win.txt")  # to load your file content into a list
    # creating fog map with the same size as labyrinth
    mapfog = blank_map(len(current_map[0]), len(current_map), F)
    spaceing = math.ceil(((len(surprise) - len(current_map) + 1) / 2))


    for i, c in enumerate(current_map):
        for z, g in enumerate(c):
            if i == 0:  # reveals map, sets player and end cordinates int variables
                mapfog[i][z] = current_map[i][z]
                mapfog[i - 1][z] = current_map[i - 1][z]
            elif z == 0:
                mapfog[i][z] = current_map[i][z]
                mapfog[i][z - 1] = current_map[i][z - 1]
            elif current_map[i][z] == P:
                py = i
                px = z
            elif current_map[i][z] == E:
                endy = i
                endx = z
    mapfog[py][px] = P
    revealrange = range(-REVEAL, REVEAL + 1)  # -1, 0, 1

    for i in current_map:  # reaveals stuff around player
        for i in revealrange:
            for z in revealrange:
                mapfog[py + i][px + z] = current_map[py + i][px + z]

    while True:  # main loop
        level_over = False
        main_print(mapfog, surprise)
        level_over = checkwin(win)
        if level_over is True:
            break
        current_map[py][px] = TRAIL  # switches player mark to trail mark
        mapfog[py][px] = current_map[py][px]
        py, px, level_over = move(current_map, py, px)
        if level_over is True:
            break
        current_map[py][px] = P  # update player position
        mapfog[py][px] = P  # update player position
        for i in revealrange:  # reaveal stuff around player
            for z in revealrange:
                mapfog[py + i][px + z] = current_map[py + i][px + z]
