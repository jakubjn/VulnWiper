import sys, os
import json
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

from UtilityClasses import *
from AIUtility import *

import Utility

class Model:
    def __init__(self):
        pass

    def _predict(self, xVal, weights):
        matrix = [line.split() for line in xVal]

        wordsToAdd = {}

        for wordArray in matrix:
            for word in wordArray:
                if(Utility.CheckForKeyValueDictionary(weights, word)):
                    print('Exists ' + word)
                else:
                    wordsToAdd[word] = 0
                    print('Added ' + word)
        
        AddWeightsWithDict(wordsToAdd)

AI = Model()     

def FixVulnerability(vulnerableDomain):
    with open(vulnerableDomain.script, 'r') as script:
        AI._predict(script, LoadWeights(vulnerableDomain.vulnerability))

FixVulnerability(VulnerableDomain("http://localhost:8000/echo", "Form XSS", "<script>alert(1);</script>", "C:\\Users\\jakub\\Documents\\TECS 2024\\SampleWebsite\\src\\EchoTest.php"))
        


