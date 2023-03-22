import os

for c in os.listdir("./"):
    print("c:", c)
    for f in os.listdir(c):
        print("f:", f)