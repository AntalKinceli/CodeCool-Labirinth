import os
import curses


def disable_curses():
    mainscreen.erase  # erases screen
    curses.nocbreak()  # disable mode
    mainscreen.keypad(False)  # disable mode
    curses.echo()  # disable mode
    curses.endwin()  # exits curses modes


def terminal_error_handler():
    disable_curses()
    print("Terminal is to small")
    input("Press Enter to exit")
    exit()


# reads map from filename and returns its values and map lines separately
def maploader(filename, border=1):
    with open(filename) as f:
        file_readout_list = f.read().splitlines()
        maplist = []  # will contain only the map
        VorL_list = []  # will contain only the variables and list/-s
        variablemark = "ß"
        f.close
        if border > 0:
            maplist.append(
                list((" " * len(file_readout_list[-1]) + "\n") * border))
        for line in file_readout_list:
            if line[:1] != variablemark:  # separates map lines and variable/list lines
                maplist.append(list(" " * border + line))  # map section
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
    try:
        for index in range(heigth):
            mainscreen.move(index + border, border)
            for z in range(width):
                mainscreen.addstr(blankmark)
    except curses.error:
        terminal_error_handler()


def drawscreen(maplist, mainscreen, border=0):  # prints map without spacing
    try:
        for index, nlist in enumerate(maplist):
            mainscreen.move(index + border, border)
            for item in nlist:
                mainscreen.addstr(item)
        mainscreen.refresh()
    except curses.error:  # handels crash if terminal is to small
        terminal_error_handler()


# handels movement, reveals in line  returns player coordinates, and boolean
def ingame_input_handler(fullmap, player_y, player_x, player_mark, reveal, mainscreen, level_shifter):
    keypressed = 410  # iddle value
    # revealoffset = 1 / not used anymore
    revealrange = range(-reveal, reveal + 1)  # -1, 0, 1 by default
    ingame_loop_continues = True
    # 113 is "q" ASCII value
    while keypressed not in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 113]:
        keypressed = mainscreen.getch()  # refresh screen
    mainscreen.addstr(player_y, player_x, TRAIL)
    if keypressed == 113:  # "q button"
        ingame_loop_continues = False
        level_shifter = False

    # UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3 just description of directions
    # d as direction
    if keypressed == curses.KEY_UP:
        DY, DX = -1, 0
        player_mark = "A"
    elif keypressed == curses.KEY_DOWN:
        DY, DX = 1, 0
        player_mark = "V"
    elif keypressed == curses.KEY_LEFT:
        DY, DX = 0, -1
        player_mark = "<"
    elif keypressed == curses.KEY_RIGHT:
        DY, DX = 0, 1
        player_mark = ">"
    elif keypressed == 113:  # 'q' button
        DY, DX = 1, 1   # can't be 0, 0
    try:
        if fullmap[player_y + DY][player_x + DX] not in WALL and ingame_loop_continues is True:
            player_y += DY
            player_x += DX
            while fullmap[player_y + DY * (reveal - 1)][player_x + DX * (reveal - 1)] not in WALL:
                for i in revealrange:
                    mainscreen.addstr(
                        player_y + DY*reveal + abs(DX)*i,
                        player_x + DX*reveal + abs(DY)*i,
                        fullmap[player_y + DY*reveal + abs(DX)*i]
                        [player_x + DX*reveal + abs(DY)*i]
                    )
                reveal += 1
        return player_y, player_x, ingame_loop_continues, player_mark, level_shifter
    except curses.error:
        terminal_error_handler()


# prints win screen and returns False if win condition is true
def checkwin(winscreen, ingame_loop_continues):
    if py == endy and px == endx:
        ingame_loop_continues = False
        curses.resizeterm(200, 200)
        mainscreen.erase()
        drawscreen(win, mainscreen)
        mainscreen.refresh()
        curses.napms(2000)

    return ingame_loop_continues


# dislpays maps in map_foldername and returns the chosen map filename, breaks the main loop if you hit "q"
def mainmenu(map_foldername, mainscreen):
    maplist = []
    mapchoose = ""
    exit_key = "q"
    try:
        # curses.resizeterm(100, 100)
        for file in os.listdir(map_foldername):  # scans for files in "maps"
            if file.endswith(".txt"):
                maplist.append(os.path.join("maps", file))
        maplist.sort()
        valid_input = [str(index) for index, item in enumerate(
            maplist)]  # only reacts to existing maps
        valid_input.append(exit_key)
        mainscreen.addstr(
            "\nWHICH LEVEL WOULD YOU LIKE TO PLAY?\n\n\nPRESS 0 FOR TUTORIAL\n\n"
        )
        for i in valid_input[1:-1]:  # from the second to the second from last
            mainscreen.addstr("PRESS " + i + " FOR LEVEL " + i + "\n\n")
        mainscreen.addstr("PRESS " + exit_key.upper() + " FOR EXIT")
        mainscreen.refresh()
        while mapchoose not in valid_input:
            mapchoose = chr(mainscreen.getch())
        mainscreen.erase()
        if mapchoose == exit_key:
            disable_curses()
            exit()
        else:
            return maplist, int(mapchoose)
    except curses.error:
        terminal_error_handler()


def reveal_aura(reveal, screen, map, player_y, player_x):
    revealrange = range(-reveal, reveal + 1)
    for i in revealrange:
        for z in revealrange:
            mainscreen.addstr(py + i, px + z, current_map[py + i][px + z])


def add_to_inventory(inventory, added_items):
    if type(added_items) == str:
        if added_items in inventory:
            inventory[added_items] += 1
        else:
            inventory[added_items] = 1
    else:
        for k in added_items:
            if k in inventory:
                inventory[k] += 1
            else:
                inventory[k] = 1


def check_stuff_on_map(mainscreen, current_map, mark_list, inventory_dict, player_y, player_x):
    if current_map[player_y][player_x] in mark_list:
        add_to_inventory(inventory_dict, mark_list[1 + mark_list.index(
            current_map[player_y][player_x])])
        mainscreen.move(0, 7)
        for k, v in inventory.items():
            mainscreen.addstr(" " + k + " : " + str(v) + " ")


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
    maplist, mapchoose = mainmenu("maps", mainscreen)

    level_shifter = True
    while level_shifter:
        # load your file content into lists and variablesmaplist[mapchoose]
        current_map, settings = maploader(maplist[mapchoose])
        (
            P,
            E,
            F,
            WALL,
            TRAIL,
            REVEAL,
            FOG,
            INVENTORY_MARKS
        ) = settings
        win = maploader("win_2.txt")[0]
        inventory = {}
        # curses.resizeterm(
        #     len(current_map) + 1, len(current_map[0]) + 1)
        # creates fog map with the same size as the current_map if enabled
        if FOG == 1:

            blank_screen(mainscreen, len(current_map[0]), len(current_map), F)
        # searches for player and endpoint marks, and accordingly sets player and endpoint coordinates 0into variables
        for Y_index, Y_item in enumerate(current_map):
            for X_index, X_item in enumerate(Y_item):
                if FOG == 1:  # reveals borders if there is fog
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
            py, px, ingame_loop, P, level_shifter = ingame_input_handler(
                current_map, py, px, P, REVEAL, mainscreen, level_shifter
            )
            # reaveals map around player in revealrange
            reveal_aura(REVEAL, mainscreen, current_map, py, px)
            # draws player mark
            check_stuff_on_map(mainscreen, current_map,
                               INVENTORY_MARKS, inventory, py, px)
            mainscreen.addstr(py, px, P)
            # sets ingame_loop False if you won, else returns ingame_loop unchanged
            ingame_loop = checkwin(win, ingame_loop)
        mainscreen.erase()
        if maplist[mapchoose] != maplist[-1]:
            mapchoose += 1
        else:
            level_shifter = False
