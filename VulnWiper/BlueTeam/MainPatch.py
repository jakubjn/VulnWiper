import sys, os
sys.path.append(os.path.abspath(os.path.join('VulnWiper')))

import Utility
from UtilityClasses import *
import BlueAI

targetProject = r'SampleWebsite'

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

