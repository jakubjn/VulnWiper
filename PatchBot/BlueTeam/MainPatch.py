import sys, os
sys.path.append(os.path.abspath(os.path.join('PatchBot')))

import Utility
from UtilityClasses import *
import BlueAI

targetProject = r'C:\Users\jakub\Documents\TECS 2024\SampleWebsite'

routes = Utility.FindRoutes(targetProject)

vulnerableDomains = Utility.LoadDomainsFromStorage()

# Check report values against routes
for route in routes.keys():
    if(Utility.CheckForDomainValue(vulnerableDomains, route) == True):
        vulnerableDomain = Utility.FindDomainValue(vulnerableDomains, route)

        vulnerableDomain.script = routes[route]

for vulnerableDomain in vulnerableDomains:
    if(vulnerableDomain.script == "null"):
        vulnerableDomains.remove(vulnerableDomain)
        continue

    BlueAI.FixVulnerability(vulnerableDomain)

