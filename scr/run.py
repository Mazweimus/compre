from collections import Counter
import json
with open("11987.jpg", "rb") as file:
    lines = file.readlines()
    la = 0
    for i in lines:
        # if la == 1:
        #     break
        print(i)
        la = la + 1
