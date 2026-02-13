from collections import Counter
with open("temporary-data/11987.jpg", "rb") as file:
    lines = file.read()
    shtm = Counter(lines)
    x = shtm.most_common()[-2]
    print(x)
    # print(shtm)

