import sys, os
import shutil

import json

import re
sys.path.append(os.path.abspath(os.path.join('VulnWiper')))

from colored_print import log
from UtilityClasses import *
from AIUtility import *

import Utility

from Tokenizer import GetTokenizer

# Tokeniser for the Code
enc = GetTokenizer()

# AI which predicts where the fix goes
class PredictionModel:
    # XValue: Script before change | YValue: Script after change

    def __init__(self, blocksize=8, error_sensitivity=10, success_sensitivity=3):
        self.error_sensitivity = error_sensitivity
        self.success_sensitivity = success_sensitivity
        self.blocksize = blocksize
        pass
    
    # Compare the script before and after, then adapt the weights
    def _train(self, xVal, yVal, vulnerability):
        weights = LoadWeights(vulnerability)

        xHash = HashBlockSizes(xVal, context_Size=self.blocksize)
        yHash = HashBlockSizes(yVal, context_Size=self.blocksize)

        #Loop through a number of contexts each time
        for context in xHash.keys():

            for token in context:
                if(Utility.CheckForKeyValueDictionary(weights, str(token)) == False):
                    weights = AddToken(token, vulnerability)

            if(context not in yHash.keys()):
                print("When the Context is: ", context)
                print("The Target is: ", 1)

                UpdateTokens(context, vulnerability, 1, self.success_sensitivity)
            else:
                print("When the Context is: ", context)
                print("The Target is: ", 0)

                UpdateTokens(context, vulnerability, -1, self.error_sensitivity)
    
    # Make a prediction on where to put the fix based on weights
    def _predict(self, xVal, vulnerability, weights):
        score = 0

        for i, token in enumerate(xVal):
            if(Utility.CheckForKeyValueDictionary(weights, str(token)) == False):
                weights = AddToken(token, vulnerability)
                continue

            if(i == 0):
                score = score + weights[str(token)]
            else:
                score = score + (weights[str(token)] / 3)

        if(score > 1): 
            score = 1
        elif(score < 0):
            score = 0

        return score
    
    def predict(self, XVal, vulnerability):
        weights = LoadWeights(vulnerability)

        best_score = 0
        best_context = []

        for i, token in enumerate(XVal):

            neighbours = GetNeighbours(i, XVal)

            array:list[int] = [token, *neighbours]

            score = self._predict(array, vulnerability, weights)

            if(score > best_score):
                best_score = score
                best_context = array

        log("Best Context: "); log.blue(enc.decode(best_context))
        log("Score: "); log.blue(best_score)

        return best_context

    def fix(self, script, context, vulnerability):
        contextString:str = context[1] + context[0] + context[2]

        script = script.replace(contextString, '')
        print(script)
        # Delete Original Context
        # Use GPT to rewrite it
        # Save the script

AI = PredictionModel(blocksize=3, error_sensitivity=150, success_sensitivity=3)    

# Trains the AI on the TrainingData
def TrainAI():
    ClearWeights()

    array = Utility.GetTrainingData(r'VulnWiper\BlueTeam\TrainingData\XSS')

    print("XSS Training")

    for fileMatrix in array:
        print("========================================")

        xVal = open(fileMatrix[0], 'r')
        yVal = open(fileMatrix[1], 'r')

        AI._train(enc.encode(xVal.read()), enc.encode(yVal.read()), "Form XSS")

        xVal.close()
        yVal.close()

# Tests the AI on the TestData
def TestAI():
    array = Utility.GetTrainingData(f'VulnWiper\BlueTeam\TestData')

    for fileMatrix in array:
        print("========================================")

        xVal = open(fileMatrix[0], 'r')

        AI.predict(enc.encode(xVal.read()), "Form XSS")

        xVal.close()

# Clones the file, predicts what part of it is broken, then fixes it
def FixVulnerability(vulnerableDomain:VulnerableDomain):
    if(vulnerableDomain.vulnerability != "Form XSS"): return

    script_Name = os.path.basename(vulnerableDomain.script)

    log('===============================')
    log.yellow(script_Name + ' | ' + vulnerableDomain.dir)

    path = shutil.copy(vulnerableDomain.script, f'VulnWiper\BlueTeam\FixedScripts\{script_Name}')
    script = open(path, 'r')
    script_read = script.read()

    context = AI.predict(enc.encode(script_read), vulnerableDomain.vulnerability)

    # AI.fix(script_read, enc.decode(context), vulnerableDomain.vulnerability)





