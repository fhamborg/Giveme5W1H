import glob
import logging
import sys

from .reader import Reader
from .writer import Writer


class Handler(object):
    def __init__(self, inputPath):

        self._inputPath = inputPath

        self._limit = None
        self._extractor = None
        self._outputPath = None
        self._adocuments = None
        self._documents = None

        self._reader = Reader()
        self._writer = Writer()
        self.log = logging.getLogger('GiveMe5W')

    def setExtractor(self, extractorFactory):
        self._extractor = extractorFactory
        return self

    def setLimit(self, limit):
        self._limit = limit
        self.log.info('document input limit:\t' + str(limit))
        return self

    def setOutputPath(self, outputPath):
        self._outputPath = outputPath
        self._writer.setOutputPath(outputPath)
        return self

    def setPreprocessedPath(self, preprocessedPath):
        # reader needs this path to read from cache
        self._reader.setPreprocessedPath(preprocessedPath)
        # writer needs  this path to write...
        self._writer.setPreprocessedPath(preprocessedPath)
        return self

    def preLoadAndCacheDocuments(self):
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

    def getDocuments(self):
        if self._documents:
            return self._documents
        else:
            self.log.error('you must call preLoadAndCacheDocuments before processing to collect the docs')

    def _processDocument(self, document):
        self.log.info('Handler: \tTitle:\t' + str(document.get_title()))
        self.log.info('         \tId:   \t' + str(document.get_document_id()))

        if self._extractor:
            if not document.is_preprocessed():
                self._extractor.preprocessor.preprocess(document)
                if self._writer.getPreprocessedPath():
                    self._writer.writePickle(document)
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

        docCounter = 0

        # process in memory objects (call preLoadDocuments)
        if self._documents:
            self.log.info('processing documents from memory')
            sys.stdout.flush()
            for document in self._documents:
                self._processDocument(document)
        else:
            self.log.info('processing documents from file system ')
            sys.stdout.flush()
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and docCounter >= self._limit:
                    print('limit reached')
                    break
                docCounter += 1
                document = self._reader.read(filepath)
                self._processDocument(document)
            self.log.info('Processed Documents:\t ' + str(docCounter))

        self.log.info('')
        self.log.info('------- Handler finished processing-------\t')
        return self
