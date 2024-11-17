import sys, os
import json

import re
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

from UtilityClasses import *
from AIUtility import *

import Utility

import tiktoken;

# Tokeniser for the Code
enc = tiktoken.get_encoding("p50k_base")
enc = tiktoken.encoding_for_model("text-davinci-003")

# AI which predicts where the fix goes
class Model:
    # XValue: Script before change | YValue: Script after change

    def __init__(self):
        pass
    
    # Compare the script before and after, then adapt the weights
    def _train(self, xVal, yVal, vulnerability):
        weights = LoadWeights(vulnerability)

        for t in range(len(xVal)):
            if(t+1 > len(xVal)): break

            if(Utility.CheckForKeyValueDictionary(weights, str(xVal[t])) == False):
                weights = AddToken(xVal[t], vulnerability)

            if(xVal[t] != yVal[t]):
                print("When the Context is: ", xVal[:t+1])
                print("The Target is: ", 1)
                print("Current Token: ", xVal[t])

                UpdateTokens(xVal[:t+1], vulnerability, 1)
                break
            else:
                print("When the Context is: ", xVal[:t+1])
                print("The Target is: ", 0)

                UpdateTokens(xVal[:t+1], vulnerability, -1)

    
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
        for t in range(len(XVal)):
            if(t+1 > len(XVal)): break

            if(Utility.CheckForKeyValueDictionary(LoadWeights(vulnerability), str(XVal[t])) == False):
                AddToken(XVal[t], vulnerability)

            score = self._predict(XVal[:t+1],vulnerability)

            if(score == 1): break

            print("For Context: ", enc.decode(XVal[:t+1]))
            print("Prediction: ", score)
  

AI = Model()    

# Trains the AI on the practice dataset
def TrainAI():
    array = Utility.GetTrainingData(r'C:\Users\jakub\Documents\TECS 2024\PatchBot\BlueTeam\TrainingData')

    for fileMatrix in array:
        print("========================================")

        xVal = open(fileMatrix[0], 'r')
        yVal = open(fileMatrix[1], 'r')

        AI._train(enc.encode(xVal.read()), enc.encode(yVal.read()), "Form XSS")

        xVal.close()
        yVal.close()

def TestAI():
    xVal = open(r'C:\Users\jakub\Documents\TECS 2024\SampleWebsite\src\EchoTest.php', 'r')

    AI.predict(enc.encode(xVal.read()), "Form XSS")

    xVal.close()

#TrainAI()




