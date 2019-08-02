import curses
import time
import math
import sys
import os
import tty
import termios
# import urwid if

# s = input("s")
# stdscr = curses.initscr()  # init curse terminal, keystorkes will be hided
# curses.noecho()  # disables any user input which is not curses
# curses.cbreak()  # unbufered input mode
# stdscr.keypad(True)  # keypad mode so speciel buttons will be returned easely
# curses.start_color()
# curses.curs_set(False)


# begin_x = 20
# begin_y = 7
# height = 5
# width = 5
# win = curses.newwin(height, width, begin_y, begin_x)
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
# stdscr.addstr(
#     "assssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss123", curses.color_pair(1))
# stdscr.refresh()
# curses.nocbreak()  # disable mode
# stdscr.keypad(False)  # disable mode
# curses.echo()  # disable mode
# # curses.endwin()  # exits curses mode

# # enters curses mode acts like try except, but stops your code no matter what
# # curses.wrapper()

# begin_x = 20
# begin_y = 7
# height = 5
# width = 40
# win = curses.newwin(height, width, begin_y, begin_x)

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


maplist = readfile("maps/00.txt")[0]
scr = curses.initscr()
y = 0
x = 0
for i in maplist:
    for z in i:
        scr.addstr(z)
    y += 1
    scr.move(y, x)
s = scr.getkey()
scr.addstr(s)
