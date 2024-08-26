class statsOBJ:
    def __init__(self):
        self.BA = None
        self.SLG = None
        self.OBP = None
        self.LOB = None
        self.RunScored = None
        self.EarnedRunScored = None
        self.PitchersUsed_against = None

        self.BA_against = None
        self.SLG_against = None
        self.OBP_against = None
        self.LOB_against = None
        self.RunScored_against = None
        self.EarnedRunScored_against = None
        self.errors = None
        self.PitchersUsed = None

        self.wins = 0

    
    def setBA(self, abs, hits):
        self.BA = hits / abs

    def setSLG(self, abs, hits, doubles, triples, hrs):
        totalBases = hits + doubles + (2 * triples) + (3 * hrs)
        self.SLG = totalBases / abs

    def setOBP(self, abs, hits, walks, hbp, sacrifices):
        self.OBP = (hits + walks + hbp) / (abs + sacrifices + walks + hbp)

    
    
    
    def setBA_against(self, abs, hits):
        self.BA_against = hits / abs

    def setSLG_against(self, abs, hits, doubles, triples, hrs):
        totalBases = hits + doubles + (2 * triples) + (3 * hrs)
        self.SLG_against = totalBases / abs

    def setOBP_against(self, abs, hits, walks, hbp, sacrifices):
        self.OBP_against = (hits + walks + hbp) / (abs + sacrifices + walks + hbp)

