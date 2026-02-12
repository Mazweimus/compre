from collections import Counter
with open("temporary-data/readme.html", "rb") as file:
    lines = file.readlines()
    la = 0
    for i in lines:
        # if la == 1:
        #     break
        print(i)
        la = la + 1
