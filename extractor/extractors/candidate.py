

class CandidatePart:
    def __init__(self):
        self._posTag = None
        self._text = None
        
    def setPosTag(self, posTag):
        self._posTag = posTag

    def getPosTag(self):
        return self._posTag

    def setText(self, text):
        self._text = text

    def getText(self):
        return self._text


   
class Candidate:
    def __init__(self):
        self._type = None
        self._raw = None
        self._score = None
        self._index = None
        self._parts = []

    def spawnPart(self):
        part = CandidatePart()
        self._parts.append(part)
        return part

    def getParts(self):
        return self._parts

    def getLegacyCandidates(self):
        return self._raw

    def setLegacyCandidates(self, raw):
        self._raw = raw

    def setType(self, type):
        self._tyoe = type

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

    def get_json(self):
        words = []
        for part in self._parts:
            words.append({ 'text': part.getText(), 'tag': part.getPosTag()})
        return {'score': self._score , 'words': words}

   
    
   