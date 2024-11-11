import json

def LoadWeights(type):
    with open(r'PatchBot\BlueTeam\Weights.json','rt') as weights:
        content = json.load(weights)
        return content[type]  
    
def AddWeightsWithDict(dict, type):
    with open(r'PatchBot\BlueTeam\Weights.json','a') as weights:
        content = json.load(weights)

        currentDict = content[type]
        dict.update(currentDict)

        content[type] = currentDict

        json.dump(content, weights, indent = 2)

