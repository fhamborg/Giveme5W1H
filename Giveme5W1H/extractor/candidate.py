from Giveme5W1H.extractor.configuration import Configuration as Config


class Candidate:
    def __init__(self):
        self._type = None
        self._raw = None
        self._score = -1

        self._index = None
        self._index_text = None

        self._parts = []
        self._lemma_count = None
        self._enhancement = {}
        self._calculations = {}
        self._config = Config.get()['candidate']

    def get_parts(self):
        return self._parts

    def set_parts(self, parts):
        self._parts = parts

    def get_parts_as_text(self):
        answer_text = []
        for part in self._parts:
            answer_text.append(part[0]['nlpToken']['originalText'])
        return ' '.join(answer_text)

    # helper to avoid refactoring by carrying data in a legacy format
    def set_raw(self, raw):
        self._raw = raw

    # helper to avoid refactoring by carrying data in a legacy format
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

    # indicated index of the first character, related to document.get_fullText()
    def set_text_index(self, index):
        self._index_text = index

    def get_text_index(self):
        return self._index_text

    # json representation for this candidate
    def get_json(self):
        if self._parts:
            json = {'parts': self._parts}
            if self._config.get('score'):
                json['score'] = self._score

            if self._config.get('text'):
                json['text'] = self.get_parts_as_text()

            if len(self._enhancement) > 0:
                json['enhancement'] = self._enhancement

            # nlpIndexSentence
            if self._index and self._config.get('nlpIndexSentence'):
                json['nlpIndexSentence'] = self._index

            if self._index_text and self._config.get('IndexText'):
                json['IndexText'] = self._index_text
            return json
        return None

    # additional information create by enhancments
    def get_enhancement(self, key):
        return self._enhancement.get(key)

    # additional information create by enhancments
    # it must be serialisable
    def set_enhancement(self, key, value):
        self._enhancement[key] = value

    def reset_enhancements(self):
        self._enhancement = {}

    def get_calculations(self, key):
        """
         helper to decouple evaluation calculations from candidate extraction
         use this for all evaluation related information
         in other words store temporal information per candidate over this interface
        :param key:
        :return:
        """
        return self._calculations[key]

    def set_calculations(self, key, value):
        self._calculations[key] = value

    def reset_calculations(self):
        self._calculations = {}

    def get_parts_character_offset(self):
        """
        returns the character offset of the first and last part.
        this span marks the candidate in the original document
        :return:
        """
        parts = self.get_parts()
        if parts:
            number_of_parts = len(parts)
            start_index = parts[0][0]['nlpToken']['characterOffsetBegin']
            end_index = None
            if len(parts) > 1:
                # more than one
                end_index = parts[number_of_parts - 1][0]['nlpToken']['characterOffsetEnd']
            else:
                # just one parts
                end_index = parts[0][0]['nlpToken']['characterOffsetEnd']
            return (start_index, end_index)
        return (-1, -1)
