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


# generates x width, y heigth list with full of g
def blank_screen(screen, width, heigth, blankmark, border=0):
    for index in range(heigth):
        mainscreen.move(index + border, border)
        for z in range(width):
            mainscreen.addstr(blankmark)


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
def ingame_input_handler(fullmap, player_y, player_x, player_mark, reveal, mainscreen):
    keypressed = -1
    revealrange = range(-reveal, reveal + 1)  # -1, 0, 1 by default
    ingame_loop_continues = True
    while keypressed == -1:
        keypressed = mainscreen.getch()
    mainscreen.addstr(player_y, player_x, TRAIL)
    if chr(keypressed) == "q":
        ingame_loop_continues = False
    elif keypressed == curses.KEY_UP and fullmap[player_y - 1][player_x] not in WALL:
        player_y -= 1
        player_mark = "A"
        while fullmap[player_y - reveal + 1][player_x] not in WALL:
            for i in revealrange:
                mainscreen.addstr(player_y - reveal, player_x + i,
                                  fullmap[player_y - reveal][player_x + i])
            reveal += 1
    elif keypressed == curses.KEY_DOWN and fullmap[player_y + 1][player_x] not in WALL:
        player_y += 1
        player_mark = "V"
        while fullmap[player_y + reveal - 1][player_x] not in WALL:
            for i in revealrange:
                mainscreen.addstr(player_y + reveal, player_x + i,
                                  fullmap[player_y + reveal][player_x + i])
            reveal += 1
    elif keypressed == curses.KEY_LEFT and fullmap[player_y][player_x - 1] not in WALL:
        player_x -= 1
        player_mark = "<"
        while fullmap[player_y][player_x - reveal + 1] not in WALL:
            for i in revealrange:
                mainscreen.addstr(player_y + i, player_x - reveal,
                                  fullmap[player_y + i][player_x - reveal])
            reveal += 1
    elif keypressed == curses.KEY_RIGHT and fullmap[player_y][player_x + 1] not in WALL:
        player_x += 1
        player_mark = ">"
        while fullmap[player_y][player_x + reveal - 1] not in WALL:
            for i in revealrange:
                mainscreen.addstr(player_y + i, player_x + reveal,
                                  fullmap[player_y + i][player_x + reveal])
            reveal += 1
    return player_y, player_x, ingame_loop_continues, player_mark


# prints win screen and returns False if win condition is true
def checkwin(winscreen, ingame_loop_continues):
    if py == endy and px == endx:
        ingame_loop_continues = False
        mainscreen.clear()
        drawscreen(win, mainscreen)
        mainscreen.refresh()
        curses.napms(2000)
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


def reveal_aura(reveal, screen, map, player_y, player_x):
    revealrange = range(-reveal, reveal + 1)
    for i in revealrange:
        for z in revealrange:
            mainscreen.addstr(py + i, px + z, current_map[py + i][px + z])


mainscreen = curses.initscr()
curses.noecho()  # limits input for curses only
curses.cbreak()  # unbufered input mode
# keypad mode so special buttons will be returned easely
mainscreen.keypad(1)
curses.start_color()  # initialize the default color set
curses.curs_set(0)  # hides cursor
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
     REVEAL,
     FOG) = settings
    win = maploader("win_2.txt")[0]

    # creates fog map with the same size as the current_map if enabled
    if FOG == 1:
        blank_screen(mainscreen, len(current_map[0]), len(current_map), F)

    # searches for player and endpoint marks, and accordingly sets player and endpoint coordinates into variables
    for Y_index, Y_item in enumerate(current_map):
        for X_index, X_item in enumerate(Y_item):
            if FOG == 1:
                if Y_index == 0 or Y_index == len(current_map) - 1:
                    mainscreen.addstr(Y_index, X_index,
                                      X_item)
                elif X_index == 0 or X_index == len(Y_item) - 1:
                    mainscreen.addstr(Y_index, X_index,
                                      X_item)
            if X_item == P:
                py = Y_index
                px = X_index
                current_map[py][px] = TRAIL
            elif X_item == E:
                endy = Y_index
                endx = X_index

    # reweals map around player in revealrange
    reveal_aura(REVEAL, mainscreen, current_map, py, px)

    # draws player mark into mainscreen according t player coordinates (py, px)
    mainscreen.addstr(py, px, P)

    # ingame loop
    ingame_loop = True
    # mainscreen.border(0)

    while ingame_loop:
        # draws trail mark on player in both map
        # waits for and handels input, refreshes main_screen, changes ingame_loop False if you hit "q"
        py, px, ingame_loop, P = ingame_input_handler(
            current_map, py, px, P, REVEAL, mainscreen)
        # reaveals map around player in revealrange
        reveal_aura(REVEAL, mainscreen, current_map, py, px)
        # draws player mark
        mainscreen.addstr(py, px, P)
        # sets ingame_loop False if you won, else returns ingame_loop unchanged
        ingame_loop = checkwin(win, ingame_loop)
    mainscreen.clear()
