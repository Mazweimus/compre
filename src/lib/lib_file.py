import time
import pickle
from collections import Counter
import os
import lib.lib_tree as lib_tree

def createCompressFile(route:str, save_route_status=False) -> None:
    """Create a compress file .barcal"""
    with open(route, "rb") as file:
        filelines = file.read()
        editableBytes = bytearray(filelines)
        shtm = Counter(filelines)
        tree = lib_tree.buildTree(shtm)
        huffTree =lib_tree.build_Huff_Tree(tree)
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
            CounterDataObject = lib_tree.createCouterBytes(shtm)
            nameOfTheFileBytes = lib_tree.turnFileNameToBytes(startOfTheFile, endOfTheFile)
            huf.write(CounterDataObject[0]) #Number of 2 bytes, that is used to know, how many cycles the compress algorithm does
            huf.write(nameOfTheFileBytes[0]) #name and path of the file
            huf.write(nameOfTheFileBytes[1]) # end of the file .
            huf.write(addedBufferMultiplier.to_bytes(1, byteorder='big'))
            huf.write(output_bytes)
            huf.write(CounterDataObject[1])
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
        strom = lib_tree.buildTree(huffTree)
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

