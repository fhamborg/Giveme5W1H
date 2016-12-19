import os
import json
from preprocessor import Preprocessor
from fiveWExtractor import FiveWExtractor
from extractors.actionExtractor import ActionExtractor

# This is just a simple example how to use the extractor

if __name__ == '__main__':
    prep = Preprocessor('/home/soeren/Downloads/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
                        '/home/soeren/Downloads/stanford-ner-2015-12-09/stanford-ner.jar')

    ex = FiveWExtractor(prep)
    for root, dir, file in os.walk('./data'):
        for name in file:
            with open(os.path.join(root, name)) as raw:
                #input('Press Enter to continue')
                data = json.load(raw)
                doc = ex.parse(data['title'], data['description'])
                bla = ActionExtractor()
                answer = doc.questions['who']
                print('------------')
                print(doc.raw_title)
                for candidate in answer:
                    print(candidate[0], ' '.join(candidate[1].leaves()), '|', ' '.join(candidate[2].leaves()))



