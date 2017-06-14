import glob
import logging
from timeit import default_timer as timer

from extractor.tools.news_please.writer import Writer
from extractor.tools.news_please.reader import Reader
from token import GREATER


class Handler(object):
    
    def __init__(self, inputPath):
       
        self._inputPath = inputPath
        
        self._limit = None
        self._extractor = None 
        self._outputPath = None
        self._processors = []
        
        self._reader = Reader()
        self._writer = Writer()
        self.log = logging.getLogger('GiveMe5W')
    
    # helper to inject any other further processing after GiveMe5W processing
    def addProcessor(self, processor):
        self._processors.append(processor)
        return self
    
    def setExtractor(self, extractor):
        self._extractor = extractor 
        return self
    
    def setLimit(self, limit):
        self._limit = limit 
        return self
    
    def setOutputPath(self, outputPath):
        self._outputPath = outputPath
        return self
    
    def preLoadAndCacheDocuments(self):
        self._documents = []
        docCounter = 0
        for filepath in glob.glob(self._inputPath + '/*.json'):
            if self._limit and docCounter >= self._limit:
                print('limit reached') 
                break
            self._documents.append(self._reader.read(filepath))
            
    def getDocuments(self):
        if self._documents:
            return self._documents
        else:
            print('you must call preLoadAndCacheDocuments before processing to collect the docs')
    
    def _processDocument(self, document):
        if self._extractor: 
            self._extractor.parse(document)
        if self._outputPath:
            self._writer.write(self._outputPath, document)
        # pass document to all registered processors
        for processor in self._processors:
                processor.process(document)
                
    def process(self):
        #timerGlobal = timer()
        docCounter = 0
        
        #process in memory objects (call preLoadDocuments)
        if self._documents:
            for document in self._documents:
                self._processDocument(document)  
        else:
        #read/instantiate them again
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and docCounter >= self._limit:
                    print('limit reached') 
                    break 
                docCounter += 1
                self._processDocument(self._reader.read(filepath))
        
        print('')   
        print('------- Handler finished processing-------\t')        
        print('Processed Documents:\t ', docCounter)        
        
                