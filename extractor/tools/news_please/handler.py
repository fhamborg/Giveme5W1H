import glob
import logging
import queue


from .reader import Reader
from .writer import Writer
import sys




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
        print('document input limit:\t', limit)
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

        print('documents prelaoded:\t', docCounter)
        return self


    def getDocuments(self):
        if self._documents:
            return self._documents
        else:
            print('you must call preLoadAndCacheDocuments before processing to collect the docs')

    def _processDocument(self, document):
        wasPreprocessed = document.is_preprocessed()
        self.log.info('Handler: ' + str(document.get_title()))
        if self._extractor:
            self._extractor.parse(document)
            if self._writer.getPreprocessedPath() and not wasPreprocessed:
                rawData = document.get_rawData()
                self._writer.writePickle(document)
                self.log.info('Handler: saved to cache')
            else:
                self.log.info('Handler: was already preprocessed')
            self.log.info('Handler: processed')

        if self._outputPath:
            self.log.info('Handler: saved to output')
            self._writer.write( document)
        self.log.info('')

    def process(self):

        docCounter = 0

        # process in memory objects (call preLoadDocuments)
        if self._documents:
            print('processing documents from memory')
            sys.stdout.flush()
            for document in self._documents:
                self._processDocument(document)
        else:
            print('processing documents from file system ')
            sys.stdout.flush()
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and docCounter >= self._limit:
                    print('limit reached')
                    break
                docCounter += 1
                document = self._reader.read(filepath)
                self._processDocument(document)
            print('Processed Documents:\t ', docCounter)

        self.log.info('')
        self.log.info('------- Handler finished processing-------\t')
        return self
