from multiprocessing.managers import BaseManager
from fileinput import filename


class DocumentManager(BaseManager):
    pass


class Document(object):
    """
    Document is a pickable container for the raw document and all related data
    """

    def __init__(self, title, desc='', text='', rawData = None):
        self._raw = {'title': title, 'description': desc, 'text': text }
        self._date = None

        self._length = 0
        self._section_offsets = []
        self._sentences = []
        self._corefs = []
        self._tokens = []
        self._posTags = []
        self._posTrees = []
        self._nerTags = []
        self._rawData = rawData
        
        self._answers = {'what': [], 'who': [], 'why': [], 'where': [], 'when': [], 'how': []}
        self._annotations = {'what': [], 'who': [], 'why': [], 'where': [], 'when': [], 'how': []}

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

    def get_answers(self):
        return self._answers

    def get_annotations(self):
        return self._annotations
    
    def get_rawData(self):
        return self._rawData

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

    def set_answer(self, question, answer):
        if question in self._answers:
            self._answers[question] = answer

    def set_annotations(self, annotations):
        self._annotations = annotations

    def pretty_answers(self):
        string = 'Answers to: "%s..."' % self.get_title()[:35]
        for question in self._answers:
            answer = 'NONE'
            if len(self._answers[question]) > 0:
                answer = self._answers[question][0]
            string += "\n\t%s:\t%s" % (question, answer)
        return string

DocumentManager.register('Document', Document)

class DocumentFactory:
    """
    DocumentFactory initializes the necessary BaseManager and allows easy instantiation of Document objects
    """

    def __init__(self):
        self.manager = DocumentManager()
        self.manager.start()

    def spawn_doc(self, title, desc=None, text=None, rawData=None):
        return self.manager.Document(title, desc or '', text or '', rawData or None)



