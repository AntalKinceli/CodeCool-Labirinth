import os
import curses


def readfile(filename):  # maploader
    with open(filename) as f:
        mixedlist = f.read().splitlines()
        maplist = []  # will contain only the map
        variablelist = []  # will contain only the variables and list/-s
        variablemark = "ß"
        f.close
        for i in mixedlist:
            if i[:1] != variablemark:  # separates map and variable/list lines
                maplist.append(list(i))  # map section
            else:  # variable/list section
                # removes variable mark on variable lefts
                j = i.lstrip(i[0])
                # removes everything on variable rights
                j = j[0:j.rfind(variablemark)]
                if j[:1] == "[":  # check if this line is list or not
                    j = j.strip("[]")  # strips "[]"
                    j = j.split(",")  # makes list from string
                    for l, k in enumerate(j):
                        if k.isdigit() is True:  # checks if list contains only digit strings
                            # converts only digit string into int
                            j[l] = (int(j[l]))
                elif j[:1].isdigit() is True:  # checks if variable contains only digit strings
                    j = int(j)  # converts only digit string into int
                variablelist.append(j)
        return maplist, variablelist


def blank_map(width, heigth, blankmark):  # generates x width, y heigth list with full of g
    blankmaplist = []
    for i in range(heigth):
        blankmaplist.append([blankmark] * width)
    return blankmaplist


def printout(maplist, mainscreen):  # prints map without spacing
    for y, i in enumerate(maplist):
        mainscreen.move(y + 1, 1)
        for z in i:
            mainscreen.addstr(z)
    mainscreen.refresh()


# handels movement, reveals in line  returns player coordinates, and boolean
def ingame_input_handler(fullmap, fogmap, player_y, player_x, revealrange, mainscreen):
    keypressed = ""
    reveal = 1
    ingame_loop_continues = True
    keypressed = mainscreen.getch()
    if keypressed == curses.KEY_BACKSPACE:
        ingame_loop_continues = False
    elif keypressed == curses.KEY_UP and fullmap[player_y - 1][player_x] not in WALL:
        player_y -= 1
        while fullmap[player_y - reveal + 1][player_x] not in WALL:
            for i in revealrange:
                fogmap[player_y - reveal][player_x +
                                          i] = fullmap[player_y - reveal][player_x + i]
            reveal += 1
    elif keypressed == curses.KEY_DOWN and fullmap[player_y + 1][player_x] not in WALL:
        player_y += 1
        while fullmap[player_y + reveal - 1][player_x] not in WALL:
            for i in revealrange:
                fogmap[player_y + reveal][player_x +
                                          i] = fullmap[player_y + reveal][player_x + i]
            reveal += 1
    elif keypressed == curses.KEY_LEFT and fullmap[player_y][player_x - 1] not in WALL:
        player_x -= 1
        while fullmap[player_y][player_x - reveal + 1] not in WALL:
            for i in revealrange:
                fogmap[player_y + i][player_x -
                                     reveal] = fullmap[player_y + i][player_x - reveal]
            reveal += 1
    elif keypressed == curses.KEY_RIGHT and fullmap[player_y][player_x + 1] not in WALL:
        player_x += 1
        while fullmap[player_y][player_x + reveal - 1] not in WALL:
            for i in revealrange:
                fogmap[player_y + i][player_x +
                                     reveal] = fullmap[player_y + i][player_x + reveal]
            reveal += 1
    return player_y, player_x, ingame_loop_continues


# prints win screen and returns False if win condition is true
def checkwin(winscreen, ingame_loop_continues):
    if py == endy and px == endx:
        ingame_loop_continues = False
    return ingame_loop_continues


# dislpays maps in mapfoldername and returns the chosen map filename, breaks the main loop if you hit "q"
def mainmenu(mapfoldername, mainscreen):
    maplist = []
    for file in os.listdir(mapfoldername):
        if file.endswith(".txt"):
            maplist.append(os.path.join("maps", file))
    maplist.sort()
    mapfilename = ""
    mm = ""
    inputindex = list(range(len(maplist)))
    for x, i in enumerate(inputindex):
        inputindex[x] = str(i)
    inputindex.append("q")
    mainscreen.addstr(
        "WHICH LEVEL WOULD YOU LIKE TO PLAY?\n\n\nPRESS 0 FOR TUTORIAL\n\n")
    for i in inputindex[1:-1]:
        mainscreen.addstr("PRESS " + i + " FOR LEVEL " + i + "\n\n")
    mainscreen.addstr("PRESS " + inputindex[-1] + " FOR EXIT")
    mainscreen.refresh()
    while mm not in inputindex:
        mm = chr(mainscreen.getch())
    if mm == "q":
        exit()
    else:
        mapfilename = maplist[int(mm)]
    mainscreen.clear()
    return mapfilename


# main loop
while True:
    mainscreen = curses.initscr()
    curses.noecho()  # disables any user input which is not curses
    curses.cbreak()  # unbufered input mode

    # dislpays maps in "maps" folder and sets your choosen map into current_map variable
    current_map = mainmenu("maps", mainscreen)

    # load your file content into lists and variables
    current_map, settings = readfile(current_map)
    (P,
     E,
     F,
     WALL,
     TRAIL,
     REVEAL) = settings
    surprise = readfile("surprise.txt")[0]
    win = readfile("win_2.txt")[0]

    # creates fog map with the same size as the current_map
    fogmap = blank_map(len(current_map[0]), len(current_map), F)

    # sets reaveal range
    revealrange = range(-REVEAL, REVEAL + 1)  # -1, 0, 1

    # reveals map edge on fogmap
    # searches for player and endpoint marks, and accordingly sets player and endpoint coordinates into variables
    for i, c in enumerate(current_map):
        for z, g in enumerate(c):
            if i == 0:
                fogmap[i][z] = current_map[i][z]
                fogmap[i - 1][z] = current_map[i - 1][z]
            elif z == 0:
                fogmap[i][z] = current_map[i][z]
                fogmap[i][z - 1] = current_map[i][z - 1]
            elif current_map[i][z] == P:
                py = i
                px = z
            elif current_map[i][z] == E:
                endy = i
                endx = z

    # draws player mark into fogmap according t player coordinates (py, px)
    fogmap[py][px] = P

    # reweals map around player in revealrange
    for i in current_map:
        for i in revealrange:
            for z in revealrange:
                fogmap[py + i][px + z] = current_map[py + i][px + z]

    # ingame loop
    ingame_loop = True
    mainscreen.border(0)
    # keypad mode so special buttons will be returned easely
    mainscreen.keypad(True)
    while ingame_loop:
        # prints fogmap
        printout(fogmap, mainscreen)
        # draws trail mark on player in both map
        current_map[py][px], fogmap[py][px] = TRAIL, TRAIL
        # waits for and handels input, changes ingame_loop False if you hit "q"
        py, px, ingame_loop = ingame_input_handler(
            current_map, fogmap, py, px, revealrange, mainscreen)
        # draws player mark in both map
        current_map[py][px], fogmap[py][px] = P, P
        # reaveals map around player in revealrange
        for i in revealrange:
            for z in revealrange:
                fogmap[py + i][px + z] = current_map[py + i][px + z]
        # sets ingame_loop False if you won, else returns ingame_loop unchanged
        ingame_loop = checkwin(win, ingame_loop)
    mainscreen.clear()
    curses.endwin()
