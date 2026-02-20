from collections import Counter
import os
with open("../temporary-data/11987.jpg", "rb") as file:
    lines = file.read()
    shtm = Counter(lines)
    num = 0
    while(True):
        # the number is 126
        # if num == 129:
        #     break
        if len(shtm) == 2:
            break
        left = shtm.most_common()[-1]
        right = shtm.most_common()[-2]
        del shtm[left[0]]
        del shtm[right[0]]
        sumValues = left[1] + right[1]
        newKey = "("+str(left[0]) + "-" + str(right[0])+")"
        shtm.update({newKey: sumValues})
        num = num + 1
    # print(newSum)

    # print(x)
    print(shtm)

