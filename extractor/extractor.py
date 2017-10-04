import logging
import queue
from threading import Thread

from combined_scoring.distance_of_candidate import DistanceOfCandidate
from extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from preprocessors.preprocessor_core_nlp import Preprocessor


class Worker(Thread):
    def __init__(self, queue):
        ''' Constructor. '''
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            extractor, document = self._queue.get()
            if extractor and document:
                extractor.extract(document)
                self._queue.task_done()


class FiveWExtractor:
    """
    The FiveWExtractor bundles all parsing modules.
    """

    log = None
    preprocessor = None
    extractors = []

    def __init__(self, preprocessor=None, extractors=None, combined_scorers=None, enhancement=None):
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

        if combined_scorers and len(combined_scorers) > 0:
            self.combinedScorers = combined_scorers
        else:
            self.log.info('No combinedScorers: initializing default configuration.')
            self.combinedScorers = [
                DistanceOfCandidate(('what', 'who'), ('how'))
            ]

        self.q = queue.Queue()

        # creating worker threads
        for i in range(len(self.extractors)):
            t = Worker(self.q)
            t.daemon = True
            t.start()

        self.enhancement = enhancement
        # check if there are enhancements
        # enhancements = Config.get().get('enhancements')
        # if enhancements:
        #     self.enhancer = []
        #     for enhancement_name in enhancements:
        #         enhancement = enhancements.get(enhancement_name)
        #         # check if a enhancement is enabled
        #         if enhancement.get('enabled'):
        #             main_module = enhancement.get('mainModule')
        #             if main_module and len(main_module) > 0:
        #                 try:
        #                     optional_import = importlib.import_module(enhancement_name+'.'+main_module)
        #                     self.enhancer.append(optional_import.Enhancement(enhancement.get('config')))
        #                 except ImportError:
        #                     self.log.error(main_module + ' import raised an exception. Is it installed?')
        #             else:
        #                 self.log.error(main_module + ' is enabled, but no mainModule string is set')
        # else:
        #     self.enhancer = None

        # if len(self.enhancer) == 0:
        #    self.log.info('No enhancement enabled')


        # if len(Config.get()['enhancer']) > 0:
        #     try:
        #         import Giveme5W_enhancer.enhancer as optional_import
        #         self.enhancer = optional_import.Enhancer()
        #     except ImportError:
        #         optional_import = None
        #         self.enhancer = optional_import
        #        self.log.info('Install giveme5W_enhancer to use enhancer functionality')
        # else:
        #     self.log.info('No enhancer')


    def preprocess(self, doc):
        if not doc.is_preprocessed():
            self.preprocessor.preprocess(doc)

            # enhancer parsing
            if self.enhancement:
                for enhancement in self.enhancement:
                    enhancement.process(doc)
        else:
            self.log.info('          \talready preprocessed')

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
        if self.combinedScorers:
            for combinedScorer in self.combinedScorers:
                combinedScorer.score(doc)
        doc.is_processed(True)

        # enhancer linking questions to data
        if self.enhancement:
            for enhancement in self.enhancement:
                enhancement.enhance(doc)

        return doc
