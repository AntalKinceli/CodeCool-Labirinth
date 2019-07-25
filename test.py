def readfile(x):  # ("") reads your x file
    with open(x) as f:
        y = f.read().splitlines()
        z = []
        h = []
        f.close
        for i in y:  # makes list array from string
            if i[:1] != "#":
                z.append(list(i))
            else:
                j = i.lstrip(i[0])
                j = j[0:j.rfind("#")]
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


labyrinth_map, settings = readfile("first_map.txt")
print(settings)
for i in settings:
    print(i)
