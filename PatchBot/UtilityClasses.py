# Class for storing domain info
class VulnerableDomain:
    def __init__(self, dir="null", vulnerability="null", payload="null", script="null"):
        self.dir = dir
        self.vulnerability = vulnerability
        self.payload = payload
        self.script = script

    def __str__(self):
        return f"({self.dir}, {self.vulnerability}, {self.payload}, {self.script})"
    
# Class for storing results of an attack
class AttackResults:
    def __init__(self, result=False, vulnerableDomain=VulnerableDomain()):
        self.result = result
        self.vulnerableDomain = vulnerableDomain

    def __str__(self):
        return f"{self.result}: {self.vulnerableDomain}"