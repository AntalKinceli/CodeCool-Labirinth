import os
for file in os.listdir("maps"):
    if file.endswith(".txt"):
        print(os.path.join("/maps", file))
