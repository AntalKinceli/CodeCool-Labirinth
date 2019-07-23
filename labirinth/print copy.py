import sys
filename = "blank_map.txt" #your file name...
LENGTH = 16
WIDTH = 80
P = "X" # player mark
Px = 10 # + 1 the reall cordinate
Py = 3 # + 1 the reall cordinate
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

MAP = readfile(filename) #calls readfile() to load your file content into a list (towrite)
MAPlist = []
for i in MAP:
    MAPlist.append([list(i)])

#map = blank_map(WIDTH, LENGTH)
#map[3][10] = "X"
MAP[Py][Px] = P
printout(MAP)
