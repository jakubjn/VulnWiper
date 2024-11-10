import sys, os
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

import requests

from bs4 import BeautifulSoup
from bs4 import Comment

import concurrent.futures

import Utility
from UtilityClasses import *
import RedAI

targetURL = "http://localhost:8000" # Target URL

subdomain_Unchecked = []
subdomain_Checked =[]

# =================================================================
# Crawling Phase

print("CRAWLING PHASE")

# Gets the subdomains of the provided domains and stores them
def EnumerateDomain(page, domain, request):
    buttons = page.find_all("a")
    results = []

    results.append(request.url)

    # Checks any buttons on the page
    for button in buttons:
        if(button.get('href')): 
            url = button.get('href')

            Utility.SanitiseURL(results, url, domain, targetURL)

    comments = page.find_all(string=lambda text: isinstance(text, Comment))

    # Checks for hidden URLs in Comments
    for comment in comments:
        if(str.find(comment, 'href="') != -1):
            start = str.find(comment, 'href="')
            end = str.rfind(comment, '"')

            url = comment[(start+6):end]

            Utility.SanitiseURL(results, url, domain, targetURL)

    # Processes the domains found
    for result in results:

        # Removes duplicate domains
        if(Utility.CheckForValue(subdomain_Unchecked, result) or Utility.CheckForValue(subdomain_Checked, result)):
            continue
        
        subdomain_Unchecked.append(result)


# Processes each Domain
def ProcessDomain(domain):
    subdomain_Checked.append(domain)
    subdomain_Unchecked.remove(domain)

    print(domain)

    request = requests.get(domain)

    if(request.status_code == 404):
        subdomain_Checked.remove(domain)
        return
    
    if(domain != request.url and Utility.CheckForValue(subdomain_Checked, request.url)):
        return

    # Reads the Website
    page = BeautifulSoup(request.content, "html.parser") 

    # Domain Enumeration
    EnumerateDomain(page, domain, request)


subdomain_Unchecked.append(targetURL)

# Crawls domains
while len(subdomain_Unchecked) > 0:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(ProcessDomain, subdomain_Unchecked)
        executor.shutdown(wait=True)

# =================================================================
# Directory Enumeration Phase

print("DIRECTORY ENUMERATION PHASE")

word_list = Utility.SplitTextFile(r'PatchBot\RedTeam\directory_wordlist.txt')

# with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#     futures = [executor.submit(requests.head, targetURL + directory) for directory in word_list]

#     # Processes all Requests
#     for future in concurrent.futures.as_completed(futures):
#         try:
#             response = future.result()
            
#             # Returns Useful Domains
#             if(response.status_code == 200 or response.status_code == 300 or response.status_code == 301 or response.status_code == 302 or response.status_code == 403):
#                 if(Utility.CheckForValue(subdomain_Unchecked, response.url) == False and Utility.CheckForValue(subdomain_Checked, response.url) == False):
#                     subdomain_Unchecked.append(response.url)

#         except requests.RequestException as e:
#             print(f"Request failed: {e}")

#     executor.shutdown(wait=True)

# # Recursively checks domains
# while len(subdomain_Unchecked) > 0:
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         executor.map(processDomain, subdomain_Unchecked)
#         executor.shutdown(wait=True)

# =================================================================
# Attack Phase

print("ATTACK PHASE")

attacked_pages = []

for domain in subdomain_Checked:
    request = requests.get(domain)

    if(Utility.CheckForDomainValue(attacked_pages, request.url)):
        continue

    print("===============================")
    print(request.url)

    page = BeautifulSoup(request.content, "html.parser") 

    attackResults = RedAI.AttackPage(request, page)

    if(attackResults == None):
        continue

    if(attackResults.result == True):
        attacked_pages.append(attackResults.vulnerableDomain)

Utility.WriteDomainsToStorage(attacked_pages)
