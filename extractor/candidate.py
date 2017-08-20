class Candidate:
    def __init__(self):
        self._type = None
        self._raw = None
        self._score = None
        self._index = None
        self._parts = None
        self._lemma_count = None
        self._calculations = {}

    def get_parts(self):
        return self._parts

    def set_parts(self, parts):
        self._parts = parts

    def set_raw(self, raw):
        self._raw = raw

    def get_raw(self):
        return self._raw

    def set_type(self, type):
        self._type = type

    def get_type(self):
        return self._type

    def set_lemma_count(self, lemma_count):
        self._lemma_count = lemma_count

    def get_lemma_count(self):
        return self._lemma_count

    def set_score(self, score):
        self._score = score

    def get_score(self):
        return self._score

    # indicated the core_nlp sentence index
    def set_sentence_index(self, index):
        self._index = index

    def get_sentence_index(self):
        return self._index

    def get_json(self):

        if self._parts:
            words = []
            for part in self._parts:
                words.append({'text': part[0], 'tag': part[1]})

            json = {'score': self._score, 'words': words}
            if self._index:
                json['nlpIndexSentence'] = self._index
            return json
        return None

    # helper to decouple evaluation calculations from candidate extraction
    # use this for all evaluation related information
    def get_calculations(self, key):
        return self._calculations[key]

    def set_calculations(self, key, value):
        self._calculations[key] = value

    def reset_calculations(self):
        self._calculations = {}
