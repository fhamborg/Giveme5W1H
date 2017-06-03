import json
import logging
from extractor.document import DocumentFactory

class Reader(object):
    
    def __init__(self):
        self.factory = DocumentFactory()
        self.log = logging.getLogger('GiveMe5W')
        
    def read(self,path):
        with open(path, encoding='utf-8') as data_file:    
            #print(data_file.read()[:11])
            data = json.load(data_file)
            
            document = self.factory.spawn_doc(data['title'],  data.setdefault('description',None) , data['text'], data)
            # load annotations if any
            if 'fiveWoneH' in data:
                annotationsForGivMe5W = {} 
                # load the questions
                for question in data['fiveWoneH']:
                    # check if there is a annotatedLiteral
                    if 'annotated' in data['fiveWoneH'][question]:
                        annotated = data['fiveWoneH'][question]['annotated']
                        # check if the literal holds data
                        if annotated is not None:
                            tmp_anno = annotationsForGivMe5W.setdefault(question,[])
                            for annotation in annotated:
                                #None, None is added for comp. reasons
                                tmp_anno.append([None,None,annotation['text']])
                document.set_annotations(annotationsForGivMe5W)
        return document