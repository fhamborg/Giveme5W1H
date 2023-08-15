class Document(object):
    """
    Document is a pickable container for the raw document and all related data
    rawData holds the native newsPlease file
    """

    def __init__(self, title='', desc='', text='', date=None, raw_data=None):

        if title is None:
            title = ''
        if desc is None:
            desc = ''
        if text is None:
            text = ''
        if date:
            self._date = date
        else:
            # use raw date as fallback if any,
            if raw_data is not None:
                self._date = raw_data.get('date_publish', None)
            else:
                self._date = None

        self._raw = {'title': title, 'description': desc, 'text': text}

        # append all document text into one string
        self._full_text = '. '.join(val for key, val in self._raw.items())

        self._file_name = None
        self._source = None

        self._length = 0
        self._section_offsets = []
        self._sentences = []
        self._corefs = []
        self._tokens = []
        self._posTags = []
        self._posTrees = []
        self._nerTags = []
        self._rawData = raw_data
        self._preprocessed = False

        self._annotations = {'what': [], 'who': [], 'why': [], 'where': [], 'when': [], 'how': []}

        self._answers = {}
        self._candidates = {}
        self._processed = None
        self._enhancement = {}

        self._error_flags = {}

    @classmethod
    def from_text(cls, text, date=None, raw_data=None):
        return cls(title=text, date=date, raw_data=raw_data)

    @classmethod
    def from_newsplease(cls, article):
        if article.date_publish:
            tmp_date = str(article.date_publish)
        else:
            tmp_date = None
        return cls(title=article.title, text=article.text, desc=article.description, date=tmp_date, raw_data=None)

    def is_preprocessed(self, preprocessed=None):
        if preprocessed is True or preprocessed is False:
            self._preprocessed = preprocessed
        return self._preprocessed

    def is_processed(self, processed=None):
        if processed is True or processed is False:
            self._processed = processed
        return self._processed

    def get_full_text(self):
        return self._full_text

    def set_candidates(self, extractor, candidates):
        self._candidates[extractor] = candidates

    def get_candidates(self, extractor: str):
        return self._candidates.get(extractor, [])

    def has_candidates(self, extractor: str):
        """
        extractor candidates prefix their candidates with  their own id
        e.g. EnvironmentExtractorNeLocatios

        this methods returns true if there is at least one candidate with the given prefix
        """
        for candidate in self._candidates:
            if candidate.startswith(extractor):
                return True
        return False

    def reset_candidates(self):
        """
        resetting candidates will force each extractor to extract them again before evaluation
        :return:
        """
        self._candidates = {}

    def get_file_name(self):
        return self._file_name

    def get_source(self):
        return self._source

    def get_len(self):
        return self._length

    def get_title(self):
        return self._raw['title']

    def get_raw(self):
        return self._raw

    def get_date(self):
        return self._date

    def get_sections(self):
        return self._section_offsets

    def get_sentences(self):
        return self._sentences

    def get_document_id(self):
        return self._rawData['dId']

    def get_corefs(self):
        return self._corefs

    def get_tokens(self):
        return self._tokens

    def get_pos(self):
        return self._posTags

    def get_trees(self):
        return self._posTrees

    def get_ner(self):
        return self._nerTags

    def get_answers(self, question=None):
        if question:
            return self._answers[question]
        else:
            return self._answers

    def get_top_answer(self, question):
        return self.get_answers(question=question)[0]

    def get_annotations(self):
        return self._annotations

    def get_rawData(self):
        return self._rawData

    def get_lemma_map(self):
        """
        Creates a map of frequency for every words per lemma

        "..he blocked me, by blocking my blocker.."
        { block: 3, me: 1  .... }
        :return:
        """
        if not hasattr(self, '_lemma_map'):
            self._lemma_map = {}
            for sentence in self._sentences:
                for token in sentence['tokens']:
                    lemma = token["lemma"]
                    lema_count = self._lemma_map.get(lemma, 0)
                    lema_count += 1
                    self._lemma_map[lemma] = lema_count

        return self._lemma_map

    def set_file_name(self, name):
        self._file_name = name

    def set_source(self, source):
        self._source = source

    def set_date(self, date):
        self._date = date

    def set_sentences(self, title, description, text):
        self._sentences = (title or []) + (description or []) + (text or [])
        self._length = len(self._sentences)

        offsets = [len(title or []), len(description or []), len(text or [])]
        offsets[1] += offsets[0]
        offsets[2] += offsets[1]
        self._section_offsets = offsets

    def set_corefs(self, corefs):
        self._corefs = corefs

    def set_tokens(self, tokens):
        self._tokens = tokens

    def set_pos(self, pos):
        self._posTags = pos

    def set_trees(self, trees):
        self._posTrees = trees

    def set_ner(self, ner):
        self._nerTags = ner

    def set_answer(self, question, candidates):
        """
        use this setter for object based answers aka list of candidate objects with proper loaded parts
        :param question:
        :param candidates:
        :return:
        """
        self._answers[question] = candidates

    def get_answer(self, question):
        return self._answers.get(question, [])

    def set_annotations(self, annotations):
        self._annotations = annotations

    def get_enhancements(self):
        """
        all additional information create by enhancements
        :param key:
        :return:
        """
        return self._enhancement

    def get_enhancement(self, key):
        """
        additional information create by enhancements
        :param key:
        :return:
        """
        return self._enhancement.get(key)

    def set_enhancement(self, key, value):
        self._enhancement[key] = value

    def reset_enhancements(self):
        self._enhancement = {}

    def set_error_flag(self, identifier):
        """
        helper to flag any processable step with error flag
        :param identifier:
        :return:
        """
        self._error_flags.setdefault(identifier, True)

    def get_error_flags(self):
        """
        helper to flag any processable step with error flag
        :param identifier:
        :return:
        """
        return self._error_flags

