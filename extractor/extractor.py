import logging
import multiprocessing

from extractor.extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from extractor.preprocessors.preprocessor_nltk import Preprocessor


class FiveWExtractor:
    """
    The FiveWExtractor bundles all parsing modules.
    """

    log = None
    preprocessor = None
    extractors = []

    def __init__(self, preprocessor, extractors=None):
        """
        Initializes the given preprocessor and extractors.

        :param extractors: List of Extractors
        :type extractors: [AbsExtractor]
        :param preprocessor: Preprocessor used to prepare the passed documents
        :type preprocessor: Preprocessor
        """

        # first initialize logger
        self.log = logging.getLogger('GiveMe5W')

        self.preprocessor = preprocessor

        # initialize extractors
        if extractors is not None and len(extractors) > 0:
            self.extractors = extractors
        else:
            # the default extractor selection
            self.log.info('No extractors passed, initializing default configuration.')
            self.extractors = [
                action_extractor.ActionExtractor(),
                environment_extractor.EnvironmentExtractor(),
                cause_extractor.CauseExtractor(),
                method_extractor.MethodExtractor()
            ]

    def parse(self, doc):
        """
        Pass a document to the preprocessor and the extractors

        :param doc: document object to parse
        :type doc: Document

        :return: the processed document
        """
        # preprocess the document
        self.preprocessor.preprocess(doc)

        # pass the document to the extractors
        threads = []
        for extractor in self.extractors:
            # every document is processed in a new thread
            t = multiprocessing.Process(target=extractor.extract, args=(doc,))
            threads.append(t)
            t.start()

        # wait for the extractors to terminate
        for t in threads:
            t.join()

        return doc
