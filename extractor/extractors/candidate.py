

class CandidatePart:
    def __init__(self):
        self._posTag = None
       
        self._text = None
        
    def setPosTag(self,posTag):
        self._postTag = posTag
    def getPosTag(self):
        return self._posTag
    
    
    
    def setText(self, text):
        self._text = text
    def getText(self):
        return self._text

   
class Candidate:
    def __init__(self, raw=None):
        self._raw = raw    
        self._score = None
        self._index = None
    
    def getRaw(self):
        return self._raw
    
    def setType(self, type):
        self._type = type
    def getType(self):
        return self._type
    
    def setScore(self, score):
        self._score = score
    def getScore(self):
        return self._score
    
    def setIndex(self, index):
        self._index = index
    def getIndex(self):
        return self._index


   
    
   