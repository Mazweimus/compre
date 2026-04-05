import heapq
from collections import Counter
import os
import json
import pickle
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
resHelp = "Compre Help>>> "


version = "0.1.0"

print(f"Welcome to COMPRE\nCAUTION: This program is case sensitive\nVersion: {version}\nFor showing all commands type \"help\"\n")
commands = {
    "q/quit": "exit the program",
    "b": "return previous command",
    "help": "show available commands",
    "compre <path>": "create a compressed file",
    "compre h": "return working direcotry in next line(can be changed by user)",
    "compre <path> ls": "list of the names of the entries in a directory",
    "compre b <path>": "return back the compressed file .barcal to normal one",
}
helpBlock = ""
historyText = ""
helpCurrentDirectoryHelpActivate = False


while True:
    if helpCurrentDirectoryHelpActivate:
        helpCurrentDirectoryHelpActivate = False
    userInput = predefined_input("Compre Terminal>> ", helpBlock)
    helpBlock = ""
    try:
        if (userInput == "quit" or userInput == "q"):
            break
        elif (userInput == "b"):
            helpBlock = historyText
        elif (userInput == "help"):
            for cmd, info in commands.items():
                print(res + cmd + " : " + info)
        elif userInput.startswith("compre") and len(userInput.split()) > 1:
            newUserInput=userInput.split()
            if (newUserInput[1] == "h"):
                helpBlock = "compre "
                helpBlock += os.getcwd()
            elif (len(newUserInput) == 3):
                if (newUserInput[2] == "ls"):
                    print(resHelp, os.listdir(newUserInput[1]))
                    helpBlock = newUserInput[0] + " " + newUserInput[1]
                elif newUserInput[1] == "b":
                    if len(newUserInput) > 2:
                        with open(newUserInput[2], "rb") as compressedFile:
                            huffTree = pickle.load(compressedFile)
                            startOfTheCompressedFile = pickle.load(compressedFile)
                            endOfTheCompressedFile = pickle.load(compressedFile)
                            padding = int.from_bytes(compressedFile.read(1), byteorder="big")
                            compressedData = compressedFile.read()
                            biteString = ""
                            for byte in compressedData:
                                biteString += bin(byte)[2:].zfill(8)

                            if padding > 0:
                                biteString = biteString[:-padding]
                            strom = buildTree(huffTree)
                            current_uzel = strom
                            latestData = bytearray()
                            for bit in biteString:
                                if bit == '0':
                                    current_uzel = current_uzel.left
                                else:
                                    current_uzel = current_uzel.right
                                    
                                if current_uzel.char is not None:
                                    latestData.append(current_uzel.char)
                                    current_uzel = strom

                            with open(startOfTheCompressedFile+endOfTheCompressedFile, "wb") as f:
                                f.write(latestData)
                    else:
                        print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
                        
                else:
                    print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
            #sdad
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
                    endOfTheFile = os.path.splitext(newUserInput[1])[1]
                    startOfTheFile = os.path.splitext(newUserInput[1])[0]
                    for byte in editableBytes:
                        normalHuffVal = huffTree[byte]
                        newBitesValues.append(normalHuffVal)
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
                        pickle.dump(shtm, huf)
                        pickle.dump(startOfTheFile, huf)
                        pickle.dump(endOfTheFile, huf)
                        huf.write(addedBufferMultiplier.to_bytes(1, byteorder='big'))
                        huf.write(output_bytes)
                    print(res + "Hotovo! Soubor naleznete v data adresáři")
        else:
            print(res+"Neplatný příkaz. Pro pomoc napište \"help\"\n")
    except Exception as e:
        print(resError,e)
    historyText = userInput