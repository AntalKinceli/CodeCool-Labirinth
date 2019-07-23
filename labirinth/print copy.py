import sys
filename = "blank_map.txt" #your file name...
def readfile(x): #("") reads your x file
    with open(x) as f:
        y = f.read().splitlines()
        z = []
        f.close
        for i in y:
            z.append(list(i))
        return z
MAP = readfile(filename) #calls readfile() to load your file content into a list (towrite)
MAPlist = []
for i in MAP:
    MAPlist.append([list(i)])

LENGTH = 16
WIDTH = 80

def blank_map(x, y):
    z = []
    for i in range(y):
        z.append(["0"] * x)
    return z
def printout(x):
    for i in x:
        print("".join(i))


#map = blank_map(WIDTH, LENGTH)
#map[3][10] = "X"
MAP[10][10] = "X"
printout(MAP)
