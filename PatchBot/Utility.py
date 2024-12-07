from bs4 import BeautifulSoup

import json

import os
import os.path

from UtilityClasses import *

htmlTagID = {
    "a": 1,
    "form": 2,
    "input": 3,
    "script": 4,
    "span": 5,
    "p": 6
}

# Adds a domain ending onto the parent url
def SanitiseURL(array, url, domain, targetURL):
    extractedDomain = " "

    if(domain != targetURL):
        extractedDomain = GetParentDomain(domain) + "/" + url
    else:
        extractedDomain = domain + url

    array.append(extractedDomain)

# Splits a text utf-8 text file by lines
def SplitTextFile(filepath):
    array = []

    f = open(filepath, encoding='utf-8')

    for line in f:
        line.split('\n')
        line = line[:len(line) - 1]
        array.append(line)

    f.close()

    return array

# Checks if a value exists inside an array
def CheckForValue(array, value):
    try:
        array.index(value)
    except:
        return False
    else:
        return True
    
def CheckForKeyValueDictionary(dict, value):
    try:
        if(dict[value] != None):
            return True;
    except:
        return False
    
    return False;

# Checks if a domain is present inside a VulnerableDomain array    
def CheckForDomainValue(array, value):
    for vulnerableDomain in array:
        if(value == vulnerableDomain.dir):
            return True
        
    return False

# Returns a VulnerableDomain if domains is present inside a VulnerableDomain array    
def FindDomainValue(array, value):
    for vulnerableDomain in array:
        if(value == vulnerableDomain.dir):
            return vulnerableDomain
        
    return None
    
# Gets the previous directory on a website
def GetParentDomain(domain):
    endPos = str.rfind(domain, '/')
    
    return domain[0:endPos]

# Write misc data to the storage
def WriteToStorage(data):
    serialised_data = json.dumps(data, indent=2)

    with open(r'PatchBot\Storage.json', 'w') as storage:
        storage.truncate()
        storage.write(serialised_data)

        storage.close()

# Parses and then writes the VulnerableDomain class to storage
def WriteDomainsToStorage(array):
    sanitised_data = {}

    for vulnerableDomain in array:
        dict = vulnerableDomain.__dict__;

        dir = dict['dir']
        dict.pop('dir')

        sanitised_data[dir] = dict;

    serialised_data = json.dumps(sanitised_data, indent=3)

    with open(r'PatchBot\Storage.json', 'w') as storage:
        storage.truncate()
        storage.write(serialised_data)

        storage.close()

# Loads misc data from the storage
def LoadStorage():
    with open(r'PatchBot\Storage.json', 'r') as storage:
        return json.load(storage)
    
# Loads domains from storage and parses them into an array of VulnerableDomain
def LoadDomainsFromStorage():
    array = []

    with open(r'PatchBot\Storage.json', 'r') as storage:
        data = json.load(storage)

        for entry in data.keys():
            values = data[entry]

            domain = VulnerableDomain(entry, values["vulnerability"], values["payload"])
            array.append(domain)

    return array


# Finds the file named routes in a project
def FindRoutes(projectPath):
    try:
        with open(projectPath + r'\routes.json', 'r') as routes:
            return json.load(routes)
    except IOError as e:
        print(e)
        print("Routes Not Found")

# Converts HTML tags into IDs and returns them
def HtmlToData(filePath):
    tag_storage = []

    with open(filePath, 'r') as file:
        page = BeautifulSoup(file, 'html.parser')
        
        for tag in page.find_all():
            if(htmlTagID.get(tag.name)):
                tag_storage.append(htmlTagID[tag.name])
        
        file.close()

    return tag_storage

# Loads data from a folder
def GetTrainingData(path):
    #["file1", "file2"],["fileX", "fileY"]

    array = []
    
    os.chdir(path)

    for file in os.listdir():
        Xfile_path = f"{path}\{file}\X.php"
        Yfile_path = f"{path}\{file}\Y.php"

        array.append([Xfile_path, Yfile_path])

    return array
