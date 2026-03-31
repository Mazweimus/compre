import heapq
from collections import Counter
import os
import json
from prompt_toolkit import prompt

 
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

def build_Huff_Tree(node, current_code="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if node is None:
        return code_dict
    if node.char is not None:
        code_dict[node.char] = current_code
        
    build_Huff_Tree(node.left, current_code + "0",  code_dict)
    build_Huff_Tree(node.right, current_code + "1", code_dict)
    return code_dict

def create_compressed_file(code_dict, previousFile):
    array = previousFile.split()

def predefined_input(normal_input, additional_input = ""):
    return prompt(normal_input, default=additional_input)

res = "Compre Response>>> "
resError = "Compre Error>>> "


version = "0.0.3.2"

print(f"Welcome to COMPRE\nCAUTION: This program is case sensitive\nVersion: {version}\nFor showing all commands type \"help\"\n")
commands = {
    "q/quit": "exit the program",
    "help": "show available commands",
    "compre <file.jpg>": "create a compressed file",
    "compre h": "return working direcotry in next line(can be changed by user)",
}
helpBlock = ""
helpCurrentDirectoryHelpActivate = False


while True:
    if helpCurrentDirectoryHelpActivate:
        helpCurrentDirectoryHelpActivate = False
    userInput = predefined_input("Compre Terminal>> ", helpBlock)
    helpBlock = ""
    try:
        if (userInput == "quit" or userInput == "q"):
            break
        elif (userInput == "help"):
            for cmd, info in commands.items():
                print(res + cmd + " : " + info)
        elif userInput.startswith("compre") and len(userInput.split()) > 1:
            newUserInput=userInput.split()
            if (newUserInput[1] == "h"):
                helpBlock = "compre "
                helpBlock += os.getcwd()
            elif(len(newUserInput) != 2):
                print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
            else:
                with open(newUserInput[1], "rb") as file:
                    filelines = file.read()
                    editableBytes = bytearray(filelines)
                    shtm = Counter(filelines)
                    print(res+" GENERATING CODE...")
                    tree = buildTree(shtm)
                    huffTree =build_Huff_Tree(tree)
                    countIndexBytes = 0
                    newBitesValues = []
                    for byte in editableBytes:
                        normalHuffVal = huffTree[byte]
                        newBitesValues.append(normalHuffVal)
                        # editableBytes[countIndexBytes] = ord(normalHuffVal)
                        countIndexBytes = countIndexBytes + 1
                    totalLenghtBytes = "".join(newBitesValues)
                    allBytes = len(totalLenghtBytes)
                    addedBufferMultiplier = 8-(allBytes % 8)
                    totalLenghtBytes += "0" * addedBufferMultiplier
                    output_bytes = bytearray()
                    for i in range(0, len(totalLenghtBytes), 8):
                        byte = int(totalLenghtBytes[i:i+8], 2)
                        output_bytes.append(byte)

                    with open("data/tree.barcal", "wb") as huf:
                        huf.write(output_bytes)
                    print(res + "Hotovo! Soubor naleznete v data adresáři")
        else:
            print(res+"Neplatný příkaz. Pro pomoc napište \"help\"\n")
    except Exception as e:
        print(resError,e)