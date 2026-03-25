import heapq
from collections import Counter
import os
import pickle
import json

 
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def buildTree(frequency):
    heap = []
    for char, freq in frequency.items():
        newNode = Node(char, freq)
        heap.append(newNode)
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        connection = Node(None, left.freq + right.freq)
        connection.left = left
        connection.right = right
        heapq.heappush(heap, connection)
    return heap[0]

def print_codes(node, current_code="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if node is None:
        return code_dict
    if node.char is not None:
        code_dict[node.char] = current_code
        
    print_codes(node.left, current_code + "0",  code_dict)
    print_codes(node.right, current_code + "1", code_dict)
    return code_dict

def create_compressed_file(code_dict, previousFile):
    array = previousFile.split()

res = "Compre Response>>> "


version = "0.0.2"

print(f"Welcome to COMPRE\nCAUTION: This program is case sensitive\nVersion: {version}\nFor showing all commands type \"help\"\n")
commands = {
    "q/quit": "exit the program",
    "help": "show available commands",
    "compre <file in public folder with type of file ext: read.jpg>": "create a compressed file",
    "compre h": "return working direcotry in next line",
}
helpBlock = ""
helpCurrentDirectoryHelpActivate = False


while True:
    if helpCurrentDirectoryHelpActivate:
        helpCurrentDirectoryHelpActivate = False
    userInput = input(str("Compre Terminal>> " + helpBlock))
    helpBlock = ""
    if (userInput == "quit" or userInput == "q"):
        break
    elif (userInput == "help"):
        for cmd, info in commands.items():
            print(res + cmd + " : " + info)
    elif userInput.startswith("compre"):
        newUserInput=userInput.split()
        if (newUserInput[1] == "h"):
            helpBlock = os.getcwd()
        elif(len(newUserInput) != 2):
            print(res + f"Zadali jste neco jineho než pattern \"compre <file in public folder with type of file etc.: read.jpg>\".Nebo pokud soubor obsahuje mezeru, tak ji prosim odstran nebo ji vymen za \"-\"\n")
        else:
            cont = False
            path = os.chdir("public/")
            dir_list =os.listdir(path)
            for file in dir_list:
                if file == newUserInput[1]:
                    cont = True
                    break
            path = os.chdir("../")
            if cont != True:
                print(res+ "Tento soubor jsem v public folderu nenasel. Zkuste zkontrolovat jestli opravdu vas soubor nebo jestli jste se nepřepsal")
            else:
                with open(newUserInput[1], "rb") as file:
                    lines = file.read()
                    shtm = Counter(lines)
                    print(res+" GENERATING CODE...")
                    tree = buildTree(shtm)
                    ass =print_codes(tree)
                    fileWithTree=json.dumps(ass)
                    with open("data/tree.txt", "w") as huf:
                        huf.write(fileWithTree)
                    print(res + "DONE! Please check the data folder for the tree. Dont worry in another update will be compressed file :))")
    else:
        print(res+"Je nám líto ale tento command jsem ve slovniku nenalezli. Pokud nevite jake jsou commandy napiste \"help\"\n")