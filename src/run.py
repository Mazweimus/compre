import heapq
from collections import Counter
import os



print("Welcome to Compre\n\nFor showing all comands type \"help\"\n")
commands = {
    "q/quit": "exit the program",
    "help": "show available commands",
}

while True:
    inta=input(str(""))
    if (inta == "quit" or inta == "q"):
        break
    print("\n" + inta + "\n")
   
# class Node:
#     def __init__(self, char, freq):
#         self.char = char
#         self.freq = freq
#         self.left = None
#         self.right = None

#     def __lt__(self, other):
#         return self.freq < other.freq

# def buildTree(frequency):
#     heap = []
#     for char, freq in frequency.items():
#         newNode = Node(char, freq)
#         newNode.append(heap)
#     heapq.heapify(heap)
#     while len(heap) > 1:
#         left = heapq.heappop()
#         right = heapq.heappop()
#         connection = Node(None, left.freq + right.freq)
#         print(left)

