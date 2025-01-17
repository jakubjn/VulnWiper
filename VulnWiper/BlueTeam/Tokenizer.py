from AIUtility import *

import re
import Utility

# Words which perform actions in the language
keywords = ['__halt_compiler', 'break', 'clone', 'die', 'empty', 'endswitch', 'final', 'function',
            'include', 'isset', 'or', 'readonly', 'switch', 'use', 'yield', 'abstract', 'callable',
            'const', 'do', 'enddeclare', 'endwhile', 'finally', 'global', 'include_once', 'list', 
            'print', 'require', 'throw', 'var', 'and', 'case', 'continue', 'echo', 'endfor', 'eval',
            'fn', 'goto', 'instanceof', 'match', 'private', 'require_once', 'trait', 'while', 'array',
            'catch', 'declare', 'else', 'endforeach', 'exit', 'for', 'if', 'insteadof', 'namespace',
            'protected', 'return', 'try', 'xor', 'as', 'class', 'default', 'elseif', 'endif', 'extends',
            'foreach', 'implements', 'interface', 'new', 'public', 'static', 'unset', 'from']

# SQL for database connections
SQL = ['SELECT', 'FROM', 'WHERE', 'ORDER', 'BY', 'AND', 'LIKE', 'OR', 'NOT', 'INSERT', 'INTO',
       'VALUES', 'IS', 'NULL', 'UPDATE', 'SET', 'UNION', 'DELETE', 'TOP', 'MAX', 'MIN', 'COUNT',
       'SUM', 'AVG', 'BETWEEN', 'AS', 'JOIN', 'INNER', 'OUTER', 'ON', 'LEFT', 'RIGHT', 'FULL', 
       'GROUP', 'HAVING', 'EXISTS', 'ANY', 'CASE', 'THEN', 'ELSE', 'END', 'CREATE', 'PROCEDURE',
       'DATABASE', 'DROP', 'TABLE', 'ALTER', 'ADD', 'CHECK', 'COLUMN', 'DELETE', 'IN']

# Global variables which the AI must know
identifiers = ['_GET', '_POST', 'GLOBALS', '_SERVER', '_FILES', '_COOKIE', '_SESSION', 
               '_REQUEST', '_ENV']

# Tokens which are used to split the code up
punctuation = ['$', '.', ',', '\\', '<', '?', '>', '&', '{', '}', '(', ')', '[', ']', '\s', '\n', '"', ' ', ';']

# Primary tokens which create other tokens
base_vocab = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
              'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', 
              '3', '4', '5', '6', '7', '8', '9', '0', '_', '-', '+', '=', '`', '~', "'", '/', '*', '!', 
              '@', '#', '%', '^', '|', ':']

def MergeTokens(array):
    newToken:str = ""

    for token in array:
        stringToken = str(token)

        newToken = newToken + stringToken

    return int(newToken)

def AssignTokenValues(array, start=0):
    dict = {}

    for i, value in enumerate(array):
        dict[value] = start+i

    return dict

# Creates Tokens based on the base_vocab
def CreateConjugateVocab(array, base_vocab):
    dict = {}

    for string in array:
        base_tokens = []

        for c in string:
            token = base_vocab[c]
            base_tokens.append(token)

        final_token = MergeTokens(base_tokens)
        dict[string] = final_token
    
    return dict

base_vocab = {**AssignTokenValues(base_vocab, start=10), **AssignTokenValues(punctuation, start=-20)}

conjugate_vocab = CreateConjugateVocab([*keywords, *identifiers, *SQL], base_vocab)

class Tokenizer:
    def __init__(self, base_vocab: dict[str:int], conjugate_vocab: dict[str:int], punctuation):
        self.base_vocab = base_vocab
        self.conjugate_vocab = conjugate_vocab
        self.punctuation = punctuation

        self.normalisation_table = AssignTokenValues([*base_vocab.values(), *conjugate_vocab.values()])

        pass

    def stringToBaseVocab(self, string):
        base_tokens = []

        for c in string:
            token = base_vocab[c]
            base_tokens.append(token)

        return base_tokens

    def splitText(self, string):
        regex:str = r""

        for i, object in enumerate(self.punctuation):
            if(i == 0):
                regex = regex + f'(\{object})'
                continue

            regex = regex + f'|(\{object})'
        
        regex += "]"

        splitText = re.split(regex, string)
        sanitisedText = []

        for text in splitText:
            if(text != None):
                sanitisedText.append(text)

        return sanitisedText
    
    def combineTokens(self, tokens):

        hash = dict()

        # Split tokens into pairs | Hash Pairs
        for i, token in enumerate(tokens):
            if(i == 0 or i == len(tokens) - 1): continue

            pair = (tokens[i-1], token)

            if pair in hash.keys():
                hash[pair] += 1
            else:
                hash[pair] = 1

        pair = None
        newToken = None

        for tuple in hash.keys():
            if(hash[tuple] <= 1): 
                continue

            merged = MergeTokens(tuple)

            if(merged >= 100000):
                continue

            pair = tuple
            newToken = merged

            break

        if(pair == None or newToken == None):
            return tokens

        copy = tokens.copy()

        # Replace all with more than one occurance
        for i, token in enumerate(tokens):
            if(i == 0 or i == len(tokens) - 1): continue

            if(tokens[i-1] == pair[0] and token == pair[1]):
                copy[i-1] = newToken
                copy[i] = 0
        
        copy = [j for i,j in enumerate(copy) if j != 0] 

        return self.combineTokens(copy)

    def encode(self, text):
        tokens = []

        split = self.splitText(text)

        for string in split:
            tokenArray = self.stringToBaseVocab(string)

            if(Utility.CheckForKeyValueDictionary(self.conjugate_vocab, string)):
                token = MergeTokens(tokenArray)
                tokens.append(token)
            else:
                for token in tokenArray: tokens.append(token)

        return tokens

    def decode(self, tokens):
        strings = []

        for token in tokens:
            if(token < 100):
                strings.append(list(base_vocab.keys())[list(base_vocab.values()).index(token)])
            else:
                mainString:str = ""
                digits = [int(i) for i in str(token)]

                for i, digit in enumerate(digits):
                    if(i != 0 and i % 2 != 0): continue

                    mergedToken = MergeTokens([digit, digits[i+1]])

                    if(mergedToken < 10): continue

                    mainString = mainString + (list(base_vocab.keys())[list(base_vocab.values()).index(mergedToken)])

                strings.append(mainString)

        return strings
    
    def decode_string(self, tokens):
        array = self.decode(tokens)

        string = ""

        for s in array:
            string += s

        return string
    
    def normaliseTokens(self, tokens):
        normalised_tokens = []

        for token in tokens:
            normalised_tokens.append(self.normalisation_table[token])

        return normalised_tokens
    
    def restoreTokens(self, normalised_tokens):
        tokens = []

        for normalised_token in normalised_tokens:
            tokens.append(list(self.normalisation_table.keys())[list(self.normalisation_table.values()).index(normalised_token)])

        return tokens

def GetTokenizer():
    return Tokenizer(base_vocab, conjugate_vocab, punctuation)