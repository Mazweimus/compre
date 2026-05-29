import heapq
from collections import Counter

class Node:
    """Je to trida na zaznamenavani uzlu v Huffman Tree"""
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
