import heapq
from collections import Counter
import os
import json
import pickle
from prompt_toolkit import prompt #TODO import ot readme that they  must to pip install prompt_toolkit
import argparse
import sys
import time

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def buildTree(frequency:Counter) -> Counter:
    """Build Huffman Tree by frequency and binary number, only in array using heapq"""
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

def build_Huff_Tree(node:Node, current_code:str="", code_dict:None=None) -> Node:
    """Recursive function to setup the tree using DFS"""
    if code_dict is None:
        code_dict = {}
    if node is None:
        return code_dict
    if node.char is not None:
        code_dict[node.char] = current_code
        
    build_Huff_Tree(node.left, current_code + "0",  code_dict)
    build_Huff_Tree(node.right, current_code + "1", code_dict)
    return code_dict

def predefined_input(normal_input:str, additional_input:str = "") -> prompt:
    """Input using last user query, that can be modifed"""
    return prompt(normal_input, default=additional_input)

commands = {
    "q/quit": "exit the program",
    "b": "return previous command",
    "help": "show available commands",
    "compre <path>": "create a compressed file",
    "compre h": "return working direcotry in next line(can be changed by user)",
    "compre <path> ls": "list of the names of the entries in a directory",
    "compre b <path>": "return back the compressed file .barcal to normal one",
}
def createCompressFile(route:str, save_route_status=False) -> None:
    """Create a compress file .barcal"""
    with open(route, "rb") as file:
        filelines = file.read()
        editableBytes = bytearray(filelines)
        shtm = Counter(filelines)
        tree = buildTree(shtm)
        huffTree =build_Huff_Tree(tree)
        countIndexBytes = 0
        newBitesValues = []
        endOfTheFile = os.path.splitext(route)[1]
        startOfTheFile = os.path.splitext(route)[0]
        osPath = startOfTheFile[::-1]
        startTime = time.time()
        maxAllowedTime = startTime+0.05
        fileName = ""
        while True:
            if time.time() > maxAllowedTime:
                raise RuntimeError("Vyprcel cas na to aby se urcila cesta, prosim zkontrolujte si, zda jste urcili dobre cestu")
            if osPath[0] == "/" or osPath[0] == "\\":
                break
            else:
                fileName += osPath[0]
                osPath = osPath[1:] 
        fileName = fileName[::-1]
        osPath = osPath[::-1]
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
        if save_route_status:
            saveRoute = save_route_status + fileName + ".barcal"
        else:
            saveRoute = osPath + "/" + fileName + ".barcal"
        with open(saveRoute, "wb") as huf:
            pickle.dump(shtm, huf)
            pickle.dump(startOfTheFile, huf)
            pickle.dump(endOfTheFile, huf)
            huf.write(addedBufferMultiplier.to_bytes(1, byteorder='big'))
            huf.write(output_bytes)
        print("Hotovo! Soubor naleznete v data adresáři")

def createNormalFile(route:str) -> None:
    """From .barcal file converts to file that was previously"""
    with open(route, "rb") as compressedFile:
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
            print("hotovo")

def CLI_interface():
    """Start the script with argparse"""
    parser = argparse.ArgumentParser(description="process file path", suggest_on_error=True)
    parser.add_argument("-r", "--route", type=str, help="route to the file")
    parser.add_argument("-b", "--route_back", type=str, help="route to the back file")
    parser.add_argument("-s", "--save_route", type=str, help="route where the file can be saved")
    args = parser.parse_args()
    
    if args.route and args.route_back:
        sys.exit("Pocet povolenych argumentu -b, -r je pouze 1")
    elif args.route:
        createCompressFile(args.route, args.route_back)
        sys.exit(0)
    elif args.route_back:
        createNormalFile(args.route_back)
    else:
        command_own_interface()


    
def command_own_interface():
    """Start the script out of the normal CLI to own"""
    res = "Compre Response>>> "
    resError = "Compre Error>>> "
    resHelp = "Compre Help>>> "


    version = "0.1.4"
    helpBlock = ""
    historyText = ""
    helpCurrentDirectoryHelpActivate = False

    print(f"Welcome to COMPRE\nCAUTION: This program is case sensitive\nVersion: {version}\nFor showing all commands type \"help\"\n")

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
                            createNormalFile(newUserInput[2])
                        else:
                            print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
                            
                    else:
                        print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
                else:
                    createCompressFile(newUserInput[1])
            else:
                print(res+"Neplatný příkaz. Pro pomoc napište \"help\"\n")
        except Exception as e:
            print(resError,e)
        historyText = userInput

CLI_interface()