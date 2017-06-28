import glob
import logging


from .writer import Writer
from .reader import Reader

class Handler(object):
    def __init__(self, inputPath):
       
        self._inputPath = inputPath
        
        self._limit = None
        self._extractor = None
        self._outputPath = None
        self._adocuments = None
        
        self._reader = Reader()
        self._writer = Writer()
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
        
        print('documents prelaoded:\t', docCounter ) 
        return self
            
    def getDocuments(self):
        if self._documents:
            return self._documents
        else:
            print('you must call preLoadAndCacheDocuments before processing to collect the docs')
    
    def _processDocument(self, document):
        
        if self._extractor: 
            self._extractor.parse(document)
            if self._reader.getPreprocessedPath():
                rawData = document.get_rawData()
                self._writer.writePickle(document, self._reader.get_preprocessedFilePath(rawData['dId']))
                
        if self._outputPath:
            self._writer.write(self._outputPath, document)
    
    
                
    def process(self):
        #timerGlobal = timer()
        docCounter = 0
        
        #process in memory objects (call preLoadDocuments)
        if self._documents:
            print('processing documents from memory')
            for document in self._documents:
                self._processDocument(document)  
        else:
            print('processing documents from file system ')
            for filepath in glob.glob(self._inputPath + '/*.json'):
                if self._limit and docCounter >= self._limit:
                    print('limit reached') 
                    break 
                docCounter += 1
                self._processDocument(self._reader.read(filepath))
            print('Processed Documents:\t ', docCounter)  
        print('')   
        print('------- Handler finished processing-------\t')        
        return self
                