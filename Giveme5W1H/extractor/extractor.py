import logging
import queue
from threading import Thread

from Giveme5W1H.extractor.combined_scoring import distance_of_candidate
from Giveme5W1H.extractor.extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from Giveme5W1H.extractor.preprocessors.preprocessor_core_nlp import Preprocessor


class Worker(Thread):
    def __init__(self, queue):
        ''' Constructor. '''
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            extractor, document = self._queue.get()
            if extractor and document:
                extractor.process(document)
                self._queue.task_done()


class MasterExtractor:
    """
    The MasterExtractor bundles all parsing modules.
    """

    log = None
    preprocessor = None
    extractors = []
    combinedScorers = None

    def __init__(self, preprocessor=None, extractors=None, combined_scorers=None, enhancement=None):
        """
         Initializes the given preprocessor and extractors.
        :param preprocessor:
        :param extractors:
        :param combined_scorers: None will load defaults, [] will run without
        :param enhancement:
        """
        # RuntimeResourcesInstaller.check_and_install()

        # first initialize logger
        self.log = logging.getLogger('GiveMe5W')

        if preprocessor:
            self.preprocessor = preprocessor
        else:
            self.preprocessor = Preprocessor('http://localhost:9000')

        # initialize extractors
        if extractors is not None and len(extractors) > 0:
            self.extractors = extractors
        else:
            # the default extractor selection
            self.log.info('No extractors passed: initializing default configuration.')
            self.extractors = [
                action_extractor.ActionExtractor(),
                environment_extractor.EnvironmentExtractor(),
                cause_extractor.CauseExtractor(),
                method_extractor.MethodExtractor()
            ]

        if combined_scorers is not None:
            self.combinedScorers = combined_scorers
        else:
            self.log.info('No combinedScorers passed: initializing default configuration.')

            self.combinedScorers = [
                # ['what'], 'how'
                distance_of_candidate.DistanceOfCandidate()
            ]

        self.q = queue.Queue()

        # creating worker threads
        for i in range(len(self.extractors)):
            t = Worker(self.q)
            t.daemon = True
            t.start()

        self.enhancement = enhancement

    def preprocess(self, doc):
        if not doc.is_preprocessed():
            self.preprocessor.preprocess(doc)

            # enhancer parsing
            if self.enhancement:
                for enhancement in self.enhancement:
                    enhancement.process(doc)

    def parse(self, doc):
        """
        Pass a document to the preprocessor and the extractors

        :param doc: document object to parse
        :type doc: Document

        :return: the processed document
        """
        # preprocess -> coreNLP and enhancer
        self.preprocess(doc)

        # run extractors in different threads
        for extractor in self.extractors:
            self.q.put((extractor, doc))

        # wait till oll extractors are done
        self.q.join()

        # apply combined_scoring
        if self.combinedScorers and isinstance(self.combinedScorers, list) and len(self.combinedScorers) > 0:
            for combinedScorer in self.combinedScorers:
                combinedScorer.score(doc)
        doc.is_processed(True)

        # enhancer: linking answers(candidate-Objects) to enhancer-data
        if self.enhancement:
            for enhancement in self.enhancement:
                enhancement.enhance(doc)

        return doc
