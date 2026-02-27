import heapq
from collections import Counter
import os

 
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

def print_codes(node, current_code=""):
    if node is not None:
        if node.char is not None:
            print(f"Byte: {node.char:<3} | Kód: {current_code}")
            
        print_codes(node.left, current_code + "0")
        print_codes(node.right, current_code + "1")

print("Welcome to Compre\n\nFor showing all comands type \"help\"\n")
commands = {
    "q/quit": "exit the program",
    "help": "show available commands",
}

while True:
    userInput = input(str("")).lower()
    if (userInput == "quit" or userInput == "q"):
        break
    elif (userInput == "help"):
        for cmd, info in commands.items():
            print(cmd + " > " + info)
    elif userInput.startswith("compre"):
        with open("temporary-data/11987.jpg", "rb") as file:
            lines = file.read()
            shtm = Counter(lines)
            print("GENERATING CODE...")
            tree = buildTree(shtm)
            print_codes(tree)
    else:
        print("\n" + userInput + "\n")
   


