import time
import pickle
from collections import Counter
import os
import sys
import lib.lib_tree as lib_tree

def createCompressFile(route:str, save_route_status=False) -> None:
    """Create a compress file .barcal"""
    if os.path.exists(route) is False:
        print("Tato cesta v tomto zarineni neexistuje")
        sys.exit(-1)
    if os.path.getsize(route) == 0:
        print("Tento soubor neobsahuje zadna data") 
        sys.exit(-1)
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
        numCheck = checkIfOsPathExistsOnBarcalFile(osPath, fileName)
        if numCheck is not None:
            fileName = fileName+"("+str(numCheck)+")"
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
            saveRoute = save_route_status + "/" + fileName + ".barcal"
        else:
            saveRoute = osPath + "/" + fileName + ".barcal"
        with open(saveRoute, "wb") as huf:
            pickle.dump(shtm, huf)
            pickle.dump(startOfTheFile, huf)
            pickle.dump(fileName, huf)
            pickle.dump(endOfTheFile, huf)
            huf.write(addedBufferMultiplier.to_bytes(1, byteorder='big'))
            huf.write(output_bytes)
        print("Hotovo! Soubor naleznete v data adresáři")

def createNormalFile(route:str) -> None:
    """From .barcal file converts to file that was previously"""
    if os.path.exists(route) is False:
        print("Tato cesta v tomto zarineni neexistuje")
        sys.exit(-1)
    if os.path.getsize(route) == 0:
        print("Tento soubor neobsahuje zadna data") 
        sys.exit(-1)
    with open(route, "rb") as compressedFile:
        huffTree = pickle.load(compressedFile)
        startOfTheCompressedFile = pickle.load(compressedFile)
        if os.path.exists(startOfTheCompressedFile) is False:
            startOfTheCompressedFile = os.getcwd()
        fileName = pickle.load(compressedFile)
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
        with open(startOfTheCompressedFile+ "/" + fileName+endOfTheCompressedFile, "wb") as f:
            f.write(latestData)
            print("hotovo")
def checkIfOsPathExistsOnBarcalFile(osPath:str, fileName:str, addition:int|None=None) -> None|int:
    """Recursive function to detect if the file exists, if yes, than the num counter start to begin"""
    returnValue = None
    if addition:
        if addition >= 1001:
            raise RuntimeError("Tento pozadavek byl ")
        if os.path.exists(osPath+fileName+"("+str(addition)+")"+".barcal"):
            additionNumPlus = addition + 1
            returnValue=checkIfOsPathExistsOnBarcalFile(osPath, fileName, additionNumPlus)
        else:
            returnValue = addition
    elif os.path.exists(osPath+fileName+".barcal"):
        returnValue = checkIfOsPathExistsOnBarcalFile(osPath, fileName, 1)
    return returnValue

# ! Functions for tar Update - not available in 1.0.X - BETA versions

def setupBytesForTar(ar_of_files:list) -> list:
    """Get bytes from file"""
    ar_of_bytes_files = []
    for route_file in ar_of_files:
        with open(route_file, "rb") as file:
            fileRead = file.read()
            editableBytes = bytearray(fileRead)
            ar_of_bytes_files.append(editableBytes)
    return ar_of_bytes_files
def putBytesTogether(ar_of_bytes:list)->bytearray:
    returnBytes = bytearray()
    for fileByte in ar_of_bytes:
        returnBytes += fileByte
    return returnBytes

def DOSMTh(oneBigByteArray:bytearray, separateArrayOfFiles:list[bytearray]):
    """Doing something for future thing"""
    oneBigByteCounter = Counter(oneBigByteArray)
    CounterTree = lib_tree.buildTree(oneBigByteCounter)
    huffTree = lib_tree.build_Huff_Tree(CounterTree)
    for fileBytes in separateArrayOfFiles:
        countIndexBytes = 0
        newBitesValues = []
        for byte in fileBytes:
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