from abc import abstractmethod

from document import Document


class AbsCombinedScoring(object):
    @abstractmethod
    def score(self, document: Document):
        pass
