import numpy
import requests
from bs4 import BeautifulSoup

import Attacks
from UtilityClasses import *

# Checks Page for SQLi Attacks and XSS
def AttackPage(request, page):
    forms = page.find_all('form')

    # Check if there's a form
    if(len(forms) > 0):  
        print("Form Found | Preparing Attacks")

        inputs = page.find_all('input')
        textareas = page.find_all('textarea')

        params = []

        # Get the parameters for the attack
        for input in inputs:
            if(input.get('name')):
                param = input.get('name')
                params.append(param)
        
        for textarea in textareas:
            if(textarea.get('name')):
                param = textarea.get('name')
                params.append(param)

        print(params)

        # Launch SQLi
        attackResult = Attacks.LaunchSQLi_Form(request, request.url, params)

        if(attackResult.result == True):
           return attackResult

        #Launch XSS
        attackResult = Attacks.LaunchXSS_Form(request, request.url, params)

        return attackResult

    # Check for params in URL
    if(str.find(request.url, '?') != -1):
        print("URL Parameters Found | Preparing Attacks")

        startPoint = str.find(request.url, '?')
        endPoint = str.find(request.url, '=')

        param = request.url[startPoint:(endPoint+1)]

        print([param])

        attackResult = Attacks.LaunchXSS_URL(request, request.url, param)

        return attackResult
    
    print("No Input Found")
    return AttackResults(False, VulnerableDomain())
