class Candidate:
    def __init__(self):
        self._type = None
        self._raw = None
        self._score = None
        self._index = None
        self._parts = None

    def getParts(self):
        return self._parts

    def setParts(self, parts):
        self._parts = parts

    def setRaw(self, raw):
        self._raw = raw

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

    def get_json(self):

        if self._parts:
            words = []
            for part in self._parts:
                words.append({'text': part[0], 'tag': part[1]})

            json = {'score': self._score, 'words': words}
            if self._index:
                json['index'] = self._index
            return json
        return None
