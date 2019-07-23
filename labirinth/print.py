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

map = blank_map(WIDTH, LENGTH)
map[3][10] = "X"
printout(map)