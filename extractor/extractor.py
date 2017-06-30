import logging

from combined_scoring.distance_of_candidate import DistanceOfCandidate
from extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from preprocessors.preprocessor_core_nlp import Preprocessor


class FiveWExtractor:
    """
    The FiveWExtractor bundles all parsing modules.
    """

    log = None
    preprocessor = None
    extractors = []
    

    def __init__(self, preprocessor=None, extractors=None, combinedScorers=None):
        """
        Initializes the given preprocessor and extractors.

        :param extractors: List of Extractors
        :type extractors: [AbsExtractor]
        :param preprocessor: Preprocessor used to prepare the passed documents
        :type preprocessor: Preprocessor
        """

        # first initialize logger
        self.log = logging.getLogger('GiveMe5W')

        if preprocessor:
            self.preprocessor = preprocessor
        else:
            self.preprocessor = Preprocessor('http://localhost:9000')

        # initialize extractors
        if extractors is not None and len(extractors) > 0:

            self.extractors = []
            for factory in extractors:
                self.extractors.append(factory())

        else:
            # the default extractor selection
            self.log.info('No extractors passed, initializing default configuration.')
            self.extractors = [
                action_extractor.factory(),
                environment_extractor.factory(),
                cause_extractor.factory(),
                method_extractor.factory()
            ]
            
        if combinedScorers and len(combinedScorers) > 0:
            self.combinedScorers = combinedScorers
        else:
            self.log.info('No combinedScorers passed, initializing default configuration.')
            self.combinedScorers = [
                DistanceOfCandidate( ('What', 'Who'),('How'), 1)
            ]
            
    def parse(self, doc):
        """
        Pass a document to the preprocessor and the extractors

        :param doc: document object to parse
        :type doc: Document

        :return: the processed document
        """
        # preprocess the document
        if not doc.is_preprocessed():
            self.preprocessor.preprocess(doc)
            self.log.debug("Preprocessor: Finished preprocessing: '%s...'" % doc.get_title()[:50])
        else:
            self.log.debug("Preprocessor: Skipped already preprocessed: '%s...'" % doc.get_title()[:50])

        for extractor in self.extractors:
            extractor.extract(doc)

        # apply combined_scoring
        if self.combinedScorers:
            for combinedScorer in self.combinedScorers:
                combinedScorer.score(doc)
        
        return doc
