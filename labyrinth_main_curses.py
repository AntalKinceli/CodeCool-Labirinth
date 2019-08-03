import os
import curses


def disable_curses():
    mainscreen.clear  # clears screen
    curses.nocbreak()  # disable mode
    mainscreen.keypad(False)  # disable mode
    curses.echo()  # disable mode
    curses.endwin()  # exits curses modes


def maploader(filename):  # reads map from filename and returns its values and map lines separately
    with open(filename) as f:
        file_readout_list = f.read().splitlines()
        maplist = []  # will contain only the map
        VorL_list = []  # will contain only the variables and list/-s
        variablemark = "ß"
        f.close
        for line in file_readout_list:
            if line[:1] != variablemark:  # separates map lines and variable/list lines
                maplist.append(list(line))  # map section
            else:  # variable/list section
                # removes variable mark on variable lefts
                VorL = line.lstrip(line[0])
                # removes everything on from the right side
                VorL = VorL[0:VorL.rfind(variablemark)]
                if VorL[:1] == "[":  # check if this is list or not
                    VorL = VorL.strip("[]")  # strips "[]"
                    VorL = VorL.split(",")  # makes list from string
                    for index, item in enumerate(VorL):
                        if item.isdigit() is True:  # checks if item in list contains only digits
                            VorL[index] = (int(VorL[index]))
                elif VorL[:1].isdigit() is True:  # checks if variable contains only digits
                    VorL = int(VorL)
                VorL_list.append(VorL)
        return maplist, VorL_list


def blank_map(width, heigth, blankmark):  # generates x width, y heigth list with full of g
    blankmaplist = []
    for i in range(heigth):
        blankmaplist.append([blankmark] * width)
    return blankmaplist


def drawscreen(maplist, mainscreen, border=0):  # prints map without spacing
    try:
        for index, nlist in enumerate(maplist):
            mainscreen.move(index + border, border)
            for item in nlist:
                mainscreen.addstr(item)
        mainscreen.refresh()
    except:  # handels crash if terminal is to small
        disable_curses()
        print("Terminal is to small")
        input("Press Enter to exit")
        exit()


# handels movement, reveals in line  returns player coordinates, and boolean
def ingame_input_handler(fullmap, fogmap, player_y, player_x, revealrange, mainscreen):
    keypressed = ""
    reveal = revealrange[-1]
    ingame_loop_continues = True
    curses.flushinp()
    keypressed = mainscreen.getch()
    if chr(keypressed) == "q":
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


# dislpays maps in map_foldername and returns the chosen map filename, breaks the main loop if you hit "q"
def mainmenu(map_foldername, mainscreen):
    maplist = []
    mapchoose = ""
    exit_key = "q"
    for file in os.listdir(map_foldername):
        if file.endswith(".txt"):
            maplist.append(os.path.join("maps", file))
    maplist.sort()
    valid_input = [str(index) for index, item in enumerate(maplist)]
    valid_input.append(exit_key)
    mainscreen.addstr(
        "WHICH LEVEL WOULD YOU LIKE TO PLAY?\n\n\nPRESS 0 FOR TUTORIAL\n\n")
    for i in valid_input[1:-1]:  # from the second to the second from last
        mainscreen.addstr("PRESS " + i + " FOR LEVEL " + i + "\n\n")
    mainscreen.addstr("PRESS " + exit_key.upper() + " FOR EXIT")
    mainscreen.refresh()
    while mapchoose not in valid_input:
        mapchoose = chr(mainscreen.getch())
    if mapchoose == exit_key:
        disable_curses()
        exit()
    else:
        mapfilename = maplist[int(mapchoose)]
    mainscreen.clear()
    return mapfilename


mainscreen = curses.initscr()
curses.noecho()  # limits input for curses only
curses.cbreak()  # unbufered input mode
# keypad mode so special buttons will be returned easely
mainscreen.keypad(True)
curses.start_color()  # initialize the default color set

# main loop
while True:

    # dislpays maps in "maps" folder on mainscreen and sets your choosen map into current_map variable
    current_map = mainmenu("maps", mainscreen)

    # load your file content into lists and variables
    current_map, settings = maploader(current_map)
    (P,
     E,
     F,
     WALL,
     TRAIL,
     REVEAL) = settings
    surprise = maploader("surprise.txt")[0]
    win = maploader("win_2.txt")[0]

    # creates fog map with the same size as the current_map
    fogmap = blank_map(len(current_map[0]), len(current_map), F)

    # sets reaveal range
    revealrange = range(-REVEAL, REVEAL + 1)  # -1, 0, 1

    # reveals map edge on fogmap
    # searches for player and endpoint marks, and accordingly sets player and endpoint coordinates into variables
    for Y_index, Y_item in enumerate(current_map):
        for X_index, X_item in enumerate(Y_item):
            if Y_index == 0:
                fogmap[Y_index][X_index] = current_map[Y_index][X_index]
                fogmap[Y_index - 1][X_index] = current_map[Y_index - 1][X_index]
            elif X_index == 0:
                fogmap[Y_index][X_index] = current_map[Y_index][X_index]
                fogmap[Y_index][X_index - 1] = current_map[Y_index][X_index - 1]
            elif current_map[Y_index][X_index] == P:
                py = Y_index
                px = X_index
            elif current_map[Y_index][X_index] == E:
                endy = Y_index
                endx = X_index

    # draws player mark into fogmap according t player coordinates (py, px)
    fogmap[py][px] = P

    # reweals map around player in revealrange
    for i in current_map:
        for i in revealrange:
            for z in revealrange:
                fogmap[py + i][px + z] = current_map[py + i][px + z]

    # ingame loop
    ingame_loop = True
    # mainscreen.border(0)
    while ingame_loop:
        # draws fogmap on mainscreen
        drawscreen(fogmap, mainscreen)
        # draws trail mark on player in both map
        current_map[py][px], fogmap[py][px] = TRAIL, TRAIL
        # waits for and handels input, refreshes main_screen, changes ingame_loop False if you hit "q"
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
