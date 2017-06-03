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
        
    def process(self):
        timerGlobal = timer()
        docCounter = 0
        #timeExtraction = 0
        for filepath in glob.glob(self._inputPath + '/*.json'):
            
            if self._limit and docCounter >= self._limit:
                print('limit reached') 
                break 
            
            docCounter += 1
            
            document = self._reader.read(filepath)
            if self._extractor: 
                self._extractor.parse(document)
            if self._outputPath:
                self._writer.write(self._outputPath, document)
            # pass document to all registered processors
            for processor in self._processors:
                processor.process(document)
        
        # todo use the logger
        #runtime = timerGlobal - timer()
        #print('All documents are processed')
        #print('All in all runtime:\t ', runtime)    
        #print('AVG extractor runtime: ', runtime)   
        print('')   
        print('------- Handler finished processing-------\t')        
        print('Processed Documents:\t ', docCounter)        
        
                