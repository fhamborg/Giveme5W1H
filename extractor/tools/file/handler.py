import glob
import logging
import os
import sys

from .reader import Reader
from .writer import Writer


class Handler(object):
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

        self.log.error('documents prelaoded:\t' + str(docCounter))
        return self

    """
    process only files without an entry in the output directory
    Warning dosent work in combination with preload_and_cache_documents,
    output is not loaded into context, if existence
    """

    def skip_documents_with_output(self, skip=True):
        self._skipDocumentsWithOutput = skip
        if not self._outputPath:
            self.log.error('Call set_output_path with a valid path, before you enable this option')
        return self

    def get_documents(self):
        if self._documents:
            return self._documents
        else:
            self.log.error('you must call preload_and_cache_documents before processing to collect the docs')

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
                self._extractor.preprocessor.preprocess(document)
            else:
                self.log.info('          \talready preprocessed')
            self._extractor.parse(document)

            self.log.info('         \tprocessed')

            # cache, after processing.
            if self._writer.get_preprocessed_path():
                self._writer.write_pickle(document)
                self.log.info('         \tsaved to cache')

        if self._outputPath:
            self.log.info('         \tsaved to output')
            self._writer.write(document)
        self.log.info('')

    def process(self):

        docCounter = 0

        # process in memory objects (call preLoadDocuments)
        if self._documents:
            self.log.info('processing documents from memory')
            self.log.info('')
            sys.stdout.flush()
            for document in self._documents:
                self._process_document(document)
        else:
            self.log.info('processing documents from file system')
            self.log.info('')
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and docCounter >= self._limit:
                    print('limit reached')
                    break
                docCounter += 1
                document = self._reader.read(filepath)
                self._process_document(document)
            self.log.info('Processed Documents:\t ' + str(docCounter))

        self.log.info('')
        self.log.info('Handler: process: finished\t')
        self.log.info('')
        return self
