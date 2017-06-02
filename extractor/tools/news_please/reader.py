import json
import logging
from extractor.document import DocumentFactory

class Reader(object):
    
    def __init__(self):
        self.factory = DocumentFactory()
        self.log = logging.getLogger('GiveMe5W')
        
    def read(self,path):
        with open(path) as data_file:    
            data = json.load(data_file)
            document = self.factory.spawn_doc(data['title'], data['description'], data['text'], data)
        return document