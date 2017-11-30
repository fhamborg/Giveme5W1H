import glob
import logging
import os
import sys

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
        docCounter = 0
        for filepath in glob.glob(self._inputPath + '/*.json'):
            if self._limit and docCounter >= self._limit:
                break
            docCounter += 1
            doc = self._reader.read(filepath);
            self._documents.append(doc)
            self.log.info('Handler: preloaded ' + doc.get_title())

        self.log.error('documents preloaded:\t' + str(docCounter))
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
                self._extractor.preprocess(document)
                # cache, after pre/processing.
                if self._writer.get_preprocessed_path():
                    self._writer.write_pickle(document)
                    self.log.info('         \tsaved to cache')
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
            sys.stdout.flush()
            for document in self._documents:
                # try:
                self._process_document(document)
                # except:
                # self.log.error('skipped one dok')

        else:
            self.log.info('processing documents from file system')
            self.log.info('')
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and doc_counter >= self._limit:
                    print('limit reached')
                    break
                doc_counter += 1
                # try:
                document = self._reader.read(filepath)
                self._process_document(document)
                # except:
                #               self.log.error('skipped one dok')

                self.log.info('==> Processed Documents:\t ' + str(doc_counter))
                self.log.info('')

        self.log.info('')
        self.log.info('Handler: process: finished\t')
        self.log.info('')
        return self
