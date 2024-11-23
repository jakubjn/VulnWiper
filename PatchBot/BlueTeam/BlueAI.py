import sys, os
import json

import re
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

from UtilityClasses import *
from AIUtility import *

import Utility

from Tokenizer import GetTokenizer

# Tokeniser for the Code
enc = GetTokenizer()

# AI which predicts where the fix goes
class Model:
    # XValue: Script before change | YValue: Script after change

    def __init__(self, blocksize=8, error_sensitivity=10, success_sensitivity=3):
        self.error_sensitivity = error_sensitivity
        self.success_sensitivity = success_sensitivity
        self.blocksize = blocksize
        pass
    
    # Compare the script before and after, then adapt the weights
    def _train(self, xVal, yVal, vulnerability):
        weights = LoadWeights(vulnerability)

        #Loop through a fixed number of tokens each time
        for i, token in enumerate(xVal):

            if(Utility.CheckForKeyValueDictionary(weights, str(token)) == False):
                weights = AddToken(token, vulnerability)

            neighbours = GetNeighbours(i, xVal)
            array = [token, *neighbours]

            if(token != yVal[i]):
                print("When the Context is: ", array)
                print("The Target is: ", 1)

                UpdateTokens(array, vulnerability, 1, self.success_sensitivity)
            else:
                print("When the Context is: ", block[:i+1])
                print("The Target is: ", 0)

                UpdateTokens(array, vulnerability, -1, self.error_sensitivity)
    
    # Make a prediction on where to put the fix based on weights
    def _predict(self, xVal, vulnerability):
        weights = LoadWeights(vulnerability)

        score = 0

        for token in xVal:
            score = score + weights[str(token)]

        if(score > 1): 
            score = 1
        elif(score < 0):
            score = 0

        return score
    
    def predict(self, XVal, vulnerability):
        blocks = GetBlocks(XVal, self.blocksize)

        for blockNum, block in enumerate(blocks):

            for i, token in enumerate(block):
                if(Utility.CheckForKeyValueDictionary(LoadWeights(vulnerability), str(token)) == False):
                    AddToken(token, vulnerability)

                score = self._predict(block[:i+1],vulnerability)

                if(score == 1): break

                print("For Context: ", enc.decode(block[:i+1]))
                print("Prediction: ", score)
  

AI = Model(blocksize=3, error_sensitivity=200, success_sensitivity=3)    

# Trains the AI on the practice dataset
def TrainAI():
    ClearWeights()

    array = Utility.GetTrainingData(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\TrainingData')

    for fileMatrix in array:
        print("========================================")

        xVal = open(fileMatrix[0], 'r')
        yVal = open(fileMatrix[1], 'r')

        AI._train(enc.encode(xVal.read()), enc.encode(yVal.read()), "Form XSS")

        xVal.close()
        yVal.close()

def TestAI():
    array = Utility.GetTrainingData(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\TestData')

    for fileMatrix in array:
        print("========================================")

        xVal = open(fileMatrix[0], 'r')

        AI.predict(enc.encode(xVal.read()), "Form XSS")

        xVal.close()

#TestAI()

TrainAI()




