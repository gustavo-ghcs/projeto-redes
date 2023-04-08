"""import os

for c in os.listdir("./"):
    print("c:", c)
    for f in os.listdir(c):
        print("f:", f)
"""

import os

listing = os.listdir()
print(listing)

for i in listing:
    print("is file:", os.path.isfile(i))
    print("abspath:", os.path.abspath(i))
    print("basename:", os.path.basename(i))
    print("commonpath:", os.path.commonpath(i))
