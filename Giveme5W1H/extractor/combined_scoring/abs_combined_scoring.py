from abc import abstractmethod

from Giveme5W1H.extractor.document import Document


class AbsCombinedScoring(object):
    @abstractmethod
    def score(self, document: Document):
        pass
