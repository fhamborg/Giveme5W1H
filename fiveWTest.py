import os
import json
from preprocessor import Preprocessor
from fiveWExtractor import FiveWExtractor
from extractors.actionExtractor import ActionExtractor

# This is just a simple example how to use the extractor

if __name__ == '__main__':
    # preprocessor expects the location of the sanford-ner.jar and a model to train the ner-parser
    # stanford-ner can be found here: http://nlp.stanford.edu/software/CRF-NER.shtml
    prep = Preprocessor('./data/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
                        './data/stanford-ner-2015-12-09/stanford-ner.jar')

    ex = FiveWExtractor(prep)

    # walks over all articles stored in data/articles, expects jsons
    for root, dir, file in os.walk('./data/articles'):
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



