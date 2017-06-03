from abc import ABCMeta, abstractmethod

class AbsProcessor:
    """
    
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, document):
        """
        Must be implemented by each Extractor
        :param document: The Document object to process
        """