import glob
import json
import logging
import os
import pickle

from .reader import Reader
from .writer import Writer


class Handler(object):
    """
    Helper to process files, this calls supports:
     - caching,
     - basic resuming abilities
     - decent logging of the process


    Handler is implementing his own workflow and wrappes only the extractor.
    Therefore handler is calling preprocess(for cache ability) by himself.
    This leads to two preprocess calls. This is fine, because every document know their state.
    """

    def __init__(self, input_path):

        self._inputPath = input_path

        self._limit = None
        self._extractor = None
        self._outputPath = None
        self._adocuments = None
        self._documents = None
        self._skipDocumentsWithOutput = False
        self._reader = Reader()
        self._writer = Writer()
        self.log = logging.getLogger('GiveMe5W')
        self._sampling = None
        self._sampling_accessor = None

    def set_extractor(self, extractor):
        self._extractor = extractor
        return self

    def set_limit(self, limit):
        self._limit = limit
        self.log.info('document input limit:\t' + str(limit))
        return self

    def set_output_path(self, output_path):
        self._outputPath = output_path
        self._writer.setOutputPath(output_path)
        return self

    def set_preprocessed_path(self, preprocessed_path):
        # reader needs this path to read from cache
        self._reader.set_preprocessed_path(preprocessed_path)
        # writer needs  this path to write...
        self._writer.set_preprocessed_path(preprocessed_path)
        return self

    def preload_and_cache_documents(self):
        self._documents = []
        doc_counter = 0
        for filepath in glob.glob(self._inputPath + '/*.json'):

            if self._limit and doc_counter >= self._limit:
                break
            if self._is_in_sample(filepath):
                doc_counter += 1
                doc = self._reader.read(filepath);
                self._documents.append(doc)
                self.log.info('Handler: preloaded ' + doc.get_title())
            else:
                self.log.info('==> Skipped not in Sample:\t ')

        self.log.error('documents preloaded:\t' + str(doc_counter))
        return self

    def skip_documents_with_output(self, skip=True):
        """
           process only files without an entry in the output directory
           Warning doesnt work in combination with preload_and_cache_documents,
           output is not loaded into context, if existence
           """
        self._skipDocumentsWithOutput = skip
        if not self._outputPath:
            self.log.error('Call set_output_path with a valid path, before you enable this option')
        return self

    def set_sampling(self, sampling: str = 'training'):
        """
        read online files with matching file identifier
        :param sampling:
        accesor
        :return:
        """
        self._sampling_accessor = sampling
        with open(self._inputPath + '/../sampling.json', encoding='utf-8') as data_file:
            self._sampling = json.load(data_file)[sampling]
        return self

    def _is_in_sample(self, file):
        """
        checks if sample is set and if given file is part of the current sample
        :param file:
        :return:
        """
        if self._sampling is None:
            return True
        elif os.path.basename(file) in self._sampling:
            return True
        else:
            return False

    def get_documents(self):
        if self._documents:
            return self._documents
        else:
            self.log.error('No documents-objects have been cached. Did you call preload_and_cache_documents?')

    def _process_document(self, document):
        self.log.info('Handler: \tTitle:\t' + str(document.get_title()))
        self.log.info('         \tId:   \t' + str(document.get_document_id()))

        if self._skipDocumentsWithOutput:
            path = self._writer._outputPath + '/' + document.get_document_id() + '.json'
            if os.path.isfile(path):
                self.log.info('         \tskipped, found result in output directory')
                self.log.info('')
                return

        if self._extractor:
            if not document.is_preprocessed():

                # coreNLP preprocessing
                self._extractor.preprocessor.preprocess(document)

                # cache, after pre/processing.
                if self._writer.get_preprocessed_path():
                    self._writer.write_pickle_file(document.get_document_id() + '/coreNLP', document)
                    self.log.info('         \tsaved to cache')

            # Enhancer
            if self._extractor.enhancement:
                for enhancement in self._extractor.enhancement:
                    enahncer_id = enhancement.get_enhancer_id()

                    # skip, if data is already present
                    if document.get_enhancement(enahncer_id):
                        continue

                    # path to cached date
                    path = self._writer._preprocessedPath + '/' + document.get_document_id() + '/' + enahncer_id + '.pickle'

                    # check if there is a cached enhancer result on disc
                    if path and os.path.isfile(path) and os.path.getsize(path) > 0:
                        with open(path, 'rb') as ff:
                            eh = pickle.load(ff)
                        document.set_enhancement(enahncer_id, eh)
                    else:
                        # create eh data
                        enhancement.process(document)
                        # cache result, if any
                        eh = document.get_enhancement(enahncer_id)
                        if eh:
                            with open(path, 'wb') as f:
                                pickle.dump(eh, f, pickle.HIGHEST_PROTOCOL)

            else:
                self.log.info('          \talready preprocessed')

            self._extractor.parse(document)
            self.log.info('         \tprocessed')

        if self._outputPath:
            self.log.info('         \tsaved to output')
            self._writer.write(document)
        self.log.info('')

    def process(self):
        doc_counter = 0
        # process in memory objects (call preLoadDocuments)
        if self._documents:
            self.log.info('processing documents from memory')
            self.log.info('')
            for document in self._documents:
                self._process_document(document)
                doc_counter += 1

                self.log.info('==> Processed Documents:\t ' + str(doc_counter))
                self.log.info('')
        else:
            self.log.info('processing documents from file system')
            self.log.info('')
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and doc_counter >= self._limit:
                    print('limit reached')
                    break
                if self._is_in_sample(filepath):
                    doc_counter += 1

                    document = self._reader.read(filepath)
                    self._process_document(document)

                    self.log.info('==> Processed Documents:\t ' + str(doc_counter))
                    self.log.info('')
                else:
                    self.log.info('==> Skipped not in Sample:\t ')

        self.log.info('')
        self.log.info('Handler: process: finished\t')
        self.log.info('')
        return self
