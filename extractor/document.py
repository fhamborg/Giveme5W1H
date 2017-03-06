from multiprocessing.managers import BaseManager


class DocumentManager(BaseManager):
    pass


class Document(object):
    def __init__(self, title, desc='', text=''):
        self._raw = {'title': title, 'description': desc, 'text': text}

        self._length = 0
        self._section_offsets = []
        self._sentences = []
        self._tokens = []
        self._posTags = []
        self._posTrees = []
        self._nerTags = []

        self._answers = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}
        self._annotations = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}

    def get_len(self):
        return self._length

    def get_title(self):
        return self._raw['title']

    def get_raw(self):
        return self._raw

    def get_sections(self):
        return self._section_offsets

    def get_sentences(self):
        return self._sentences

    def get_tokens(self):
        return self._tokens

    def get_pos(self):
        return self._posTags

    def get_trees(self):
        return self._posTrees

    def get_ner(self):
        return self._nerTags

    def get_answers(self):
        return self._answers

    def get_annotations(self):
        return self._annotations

    def set_sentences(self, title, description, text):
        self._sentences = (title or []) + (description or []) + (text or [])
        self._length = len(self._sentences)

        offsets = [len(title or []), len(description or []), len(text or [])]
        offsets[1] += offsets[0]
        offsets[2] += offsets[1]
        self._section_offsets = offsets

    def set_tokens(self, tokens):
        self._tokens = tokens

    def set_pos(self, pos):
        self._posTags = pos

    def set_trees(self, trees):
        self._posTrees = trees

    def set_ner(self, ner):
        self._nerTags = ner

    def set_answer(self, question, answer):
        if question in self._answers:
            self._answers[question] = answer

    def set_annotations(self, annotations):
        self._annotations = annotations

DocumentManager.register('Document', Document)

class DocumentFactory:
    def __init__(self):
        self.manager = DocumentManager()
        self.manager.start()

    def spawn_doc(self, title, desc=None, text=None):
        return self.manager.Document(title, desc or '', text or '')



