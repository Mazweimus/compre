import heapq
from collections import Counter
import os
import pickle
import tomllib

 
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
    return(heap[0])

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
    
with open("config.toml", "rb") as f:
    config = tomllib.load(f) 

print(f"Welcome to {config['name']}\nVersion: {config['Version']}\nFor showing all comands type \"help\"\n")
commands = {
    "q/quit": "exit the program",
    "help": "show available commands",
    "compre": "create a compressed file"
}

while True:
    userInput = input(str("Compre Terminal>> ")).lower()
    if (userInput == "quit" or userInput == "q"):
        break
    elif (userInput == "help"):
        for cmd, info in commands.items():
            print(cmd + " > " + info)
    elif userInput.startswith("compre"):
        with open("temporary-data/11987.jpg", "rb") as file:
            lines = file.read()
            print(lines)
            shtm = Counter(lines)
            print("GENERATING CODE...")
            tree = buildTree(shtm)
            ass =print_codes(tree)
            print("DONE!")
    else:
        print("\n" + userInput + "\n")
   


