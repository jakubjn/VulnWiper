from AIUtility import *

import re
import Utility

# Words which perform actions in the language
keywords = ['__halt_compiler', 'break', 'clone', 'die', 'empty', 'endswitch', 'final', 'function',
            'include', 'isset', 'or', 'readonly', 'switch', 'use', 'yield from', 'abstract', 'callable',
            'const', 'do', 'enddeclare', 'endwhile', 'finally', 'global', 'include_once', 'list', 
            'print', 'require', 'throw', 'var', 'and', 'case', 'continue', 'echo', 'endfor', 'eval',
            'fn', 'goto', 'instanceof', 'match', 'private', 'require_once', 'trait', 'while', 'array',
            'catch', 'declare', 'else', 'endforeach', 'exit', 'for', 'if', 'insteadof', 'namespace',
            'protected', 'return', 'try', 'xor', 'as', 'class', 'default', 'elseif', 'endif', 'extends',
            'foreach', 'implements', 'interface', 'new', 'public', 'static', 'unset', 'yield']

# Global variables which the AI must know
identifiers = ['_GET', '_POST', 'GLOBALS', '_SERVER', '_FILES', '_COOKIE', '_SESSION', 
               '_REQUEST', '_ENV']

# Tokens which are used to split the code up
punctuation = ['\$', '\.', '\,', '\<', '\?', '\>', '\&', '\{', '\}', '\(', '\)', '\[', '\]', '\s', '\n', '\"']

# Primary tokens which create other tokens
base_vocab = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
              'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', 
              '3', '4', '5', '6', '7', '8', '9', '0', '_', '-', '+', '=', '`', '~', '"', "'", '/', '*', 
              '!', '@', '#', '%', '^', ';', '|', ':', '$', '.', ',', '<', '?', '>', '&', '{', '}', '(',
              ')', '[', ']', '\s', '\n', ' ']

def MergeTokens(array):
    newToken:str = ""

    for token in array:
        stringToken = str(token)

        newToken = newToken + stringToken

    return int(newToken)

def AssignTokenValues(array, start=0):
    dict = {}

    for i, string in enumerate(array):
        dict[string] = start+i

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

base_vocab = AssignTokenValues(base_vocab, start=10)
conjugate_vocab = CreateConjugateVocab([*keywords, *identifiers], base_vocab)

class Tokenizer:
    def __init__(self, base_vocab: dict[str:int], conjugate_vocab: dict[str:int], punctuation):
        self.base_vocab = base_vocab
        self.conjugate_vocab = conjugate_vocab
        self.punctuation = punctuation
        pass

    def stringToBaseVocab(self, string):
        base_tokens = []

        for c in string:
            token = base_vocab[c]
            base_tokens.append(token)

        return base_tokens

    def splitText(self, string):
        regex:str = ""

        for i, object in enumerate(self.punctuation):
            if(i != 0):
                regex = regex + f'|{object}'
            else:
                regex = regex + f'{object}'

        splitText = re.split(regex, string)
        sanitisedText = []

        for text in splitText:
            if(text != ''):
                sanitisedText.append(text)

        return sanitisedText

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

def GetTokenizer():
    return Tokenizer(base_vocab, conjugate_vocab, punctuation)