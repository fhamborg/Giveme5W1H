from abc import abstractmethod

from extractor.document import Document


class AbsCombinedScoring(object):
    @abstractmethod
    def score(self, document: Document):
        pass
