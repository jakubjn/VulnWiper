import sys, os
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

import json
import numpy

import Utility

class ContextValuePair:
    def __init__(self, key, value):
        self.Key = key
        self.Value = value

    def ToDict(self):
        return {"Key":self.Key, "Value":self.Value}

# Loads a specific type of weights
def LoadWeights(type):
    with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Weights.json','rt') as weights:
        content = json.load(weights)
        return content[type]  

# Loads the entire content of the weights   
def LoadContent():
    with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Weights.json','rt') as weights:
        content = json.load(weights)
        return content 
    
def LoadPatch(type):
     with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Patches.json','rt') as patches:
        content = json.load(patches)
        return content[type]
    
def ClearWeights():
    with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Weights.json','w') as weights:
        content = {}

        content["Form XSS"] = {"0" : 0}
        content["Form SQLi"] = {"0" : 0}
        content["URL XSS"] = {"0" : 0}

        json.dump(content, weights, indent = 2)

# Removes unneccessary entries and characters from tokens 
def SanitiseLines(matrix):
    for line in matrix:
        wordsToRemove = []

        for word in line:
            if(str.find(word, '"', 0, 1) != -1):
                wordsToRemove.append(word)
                continue

            if(str.find(word, "'", 0, 1) != -1):
                wordsToRemove.append(word)
                continue

            if(len(word) < 3):
                wordsToRemove.append(word)

        for word in wordsToRemove:
            line.remove(word)

# Returns the words which appear in both matrixes
def FindSameCharacters(matrixX, matrixY):
    length = min(len(matrixX), len(matrixY))

    characters = []

    for i in range(length):
        line = matrixX[i]

        for word in line:
            if(Utility.CheckForValue(matrixY[i], word)):
                characters.append(word)

    return characters

# Adds tokens to the weights dictionary    
def AddWeightsWithDict(dict, type):
    content = LoadContent()

    with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Weights.json','w') as weights:
        currentDict = content[type]

        content[type] = currentDict | dict

        weights.truncate()

        json.dump(content, weights, indent = 2)

def AddToken(token, type):
    content = LoadContent()

    with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Weights.json','w') as weights:
        currentDict = content[type]

        currentDict[token] = 0

        content[type] = currentDict

        weights.truncate()

        json.dump(content, weights, indent = 2)

        return content[type]

def UpdateToken(token, position, type, discriminant=1, sensitivity=3):
    #Discriminant: Whether the value should trend to negative or positive
    #Sensitivity: How much the value is affected
    #Position: How far the value is from the current token

    content = LoadContent()

    with open(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\Weights.json','w') as weights:
        currentDict = content[type]

        currentDict[str(token)] = currentDict[str(token)] + discriminant * (1 / (position * sensitivity))

        content[type] = currentDict

        weights.truncate()

        json.dump(content, weights, indent = 2)

        return content[type]

# Updates multiple tokens
def UpdateTokens(tokens, type, discriminant=1, sensitivity=3):
    for i, token in enumerate(tokens):
        if(token < 0): continue

        UpdateToken(token, i+1, type, discriminant, sensitivity)

# Splits a token array into a given block size
def GetBlocks(array, blocksize):
    matrix = [] 

    length = len(array)

    while blocksize < length:
        newArray = array[:blocksize]
        matrix.append(newArray)

        for i in range(blocksize): 
            array.pop(0)
        
        length = len(array)
    
    if(length > 1):
        newArray = array[:length]
        matrix.append(newArray)

    return matrix

def GetNeighbours(i, array):
    length = len(array) - 1

    if(i-1 >= 0 and i+1 <= length):
        return [array[i-1], array[i+1]]
    elif(i-1 < 0):
        return [array[i+1]]
    elif(i+1 > length):
        return [array[i-1]]
    
    print("No Neighbours?", i)

def HashBlockSizes(xVal, context_Size=2):
    hash = dict()

    # Split tokens into pairs | Hash Pairs
    for i, token in enumerate(xVal):
        if(i < context_Size or i == (len(xVal) - 1)): continue

        pair = []

        for context in range(context_Size):
            pair.append(xVal[i-context])

        pair = tuple(pair)

        if pair in hash.keys():
            hash[pair] += 1
        else:
            hash[pair] = 1

    return hash

