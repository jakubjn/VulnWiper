import sys, os
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

from UtilityClasses import *

class Model:
    def __init__(self):
        pass

    def _train(xVal, yVal):
        # Give the AI an X Value, then check it with the Y Value

        # Adapt the weights to match the Y Value

        pass

    def _predict(xVal):
        # Use a function to predict the y value with the weights

        pass

    def predict(xValues):
        # Predict multiple x Values 

        pass

AI = Model()

def FixVulnerability(vulnerableDomain):
    with open(vulnerableDomain.script, 'rt') as script:
        print(script.read())

        script.close()


