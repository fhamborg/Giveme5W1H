import glob
import logging
import queue
from threading import Thread

from .reader import Reader
from .writer import Writer

# global working qeue
q = queue.Queue()


def worker():
    while True:
        document = q.get()
        print(document.get_title())
        q.task_done()


class MyThread(Thread):
    def __init__(self, extractor, writer):
        ''' Constructor. '''
        Thread.__init__(self)
        self._extractor = extractor
        self._writer = writer

    def run(self):
        while True:
            document = q.get()
            wasPreprocessed = document.is_preprocessed()

            if self._extractor:
                self._extractor.parse(document)
                if self._writer.getPreprocessedPath() and not wasPreprocessed:
                    rawData = document.get_rawData()
                    self._writer.writePickle(document, self._writer.get_preprocessedFilePath(rawData['dId']))

            self._writer.write(document)
            q.task_done()


class Handler(object):
    def __init__(self, inputPath):

        self._inputPath = inputPath

        self._limit = None
        self._extractor = None
        self._outputPath = None
        self._adocuments = None
        self._documents = None

        self._reader = Reader()
        #self._writer = Writer()
        self.log = logging.getLogger('GiveMe5W')

    def setExtractor(self, extractor):
        self._extractor = extractor
        return self

    def setLimit(self, limit):
        self._limit = limit
        print('document input limit:\t', limit)
        return self

    def setOutputPath(self, outputPath):
        self._outputPath = outputPath
        return self

    def setPreprocessedPath(self, preprocessedPath):
        self._reader.setPreprocessedPath(preprocessedPath)
        return self

    def preLoadAndCacheDocuments(self):
        self._documents = []
        docCounter = 0
        for filepath in glob.glob(self._inputPath + '/*.json'):
            if self._limit and docCounter >= self._limit:
                break
            docCounter += 1
            self._documents.append(self._reader.read(filepath))

        print('documents prelaoded:\t', docCounter)
        return self

    def getDocuments(self):
        if self._documents:
            return self._documents
        else:
            print('you must call preLoadAndCacheDocuments before processing to collect the docs')

    def _processDocument(self, document):

        wasPreprocessed = document.is_preprocessed()

        if self._extractor:
            self._extractor.parse(document)
            if self._reader.getPreprocessedPath() and not wasPreprocessed:
                rawData = document.get_rawData()
                self._writer.writePickle(document, self._reader.get_preprocessedFilePath(rawData['dId']))

        if self._outputPath:
            self._writer.write(self._outputPath, document)


    def process(self):


        docCounter = 0

        # process in memory objects (call preLoadDocuments)
        if self._documents:
            print('processing documents from memory')
            for document in self._documents:
                q.put(document)
                # self._processDocument(document)
        else:
            print('processing documents from file system ')
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and docCounter >= self._limit:
                    print('limit reached')
                    break
                docCounter += 1
                document = self._reader.read(filepath)
                q.put(document)
                # self._processDocument(document)
            print('Processed Documents:\t ', docCounter)

        # spawn threads
        for i in range(4):
            t = MyThread(self._extractor, Writer(self._outputPath ,self._reader.get_preprocessedFilePath))
            t.daemon = True
            t.start()

        # wait until all threads are done
        q.join()
        print('')
        print('------- Handler finished processing-------\t')
        return self
