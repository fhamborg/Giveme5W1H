import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractors.abs_extractor import AbsExtractor
from extractor.extractor import FiveWExtractor
from extractor.tools import gate_reader

"""
This extractor actually measures the distance between named entities of the same type.

"""

abs_path = '/'.join(os.path.realpath(__file__).split('/')[:-3])
# path to dir with documents
document_path = abs_path + '/examples/sample_articles/'
# path were to save results
result_path = abs_path + '/examples/'


class NERD(AbsExtractor):
    def __init__(self, csv, tags):
        self.pairs = []
        self.csv = csv
        self.tags = tags

    def extract(self, document):
        """
         Measures distance between named entities of the same type

         :param document: Document to examine
         :type document: Document

         :return: The examined document
        """

        for sentence in document.get_ner():
            first = None
            for i in range(len(sentence)):
                if sentence[i][1] in self.tags:
                    if first is None:
                        # entity of new type found
                        first = (i, sentence[i][1])
                    else:
                        self.csv.write(';'.join([first[1], sentence[i][1], str(i - first[0]),
                                       ' '.join([t[0] for t in sentence[first[0]:i+1]])]) + '\n')
                        first = (i, sentence[i][1])

        return document

if __name__ == '__main__':

    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    # Host of the CoreNLP server
    # For information on how to build/run a CoreNLP instance go to: https://stanfordnlp.github.io/CoreNLP/
    core_nlp_host = 'localhost:9000'
    preprocessor = Preprocessor(core_nlp_host)

    with open(result_path + 'nerd_loc.csv', 'w+') as csv_loc:
        with open(result_path + 'nerd_time.csv', 'w+') as csv_time:

            # initialize NERD object for time and location
            nerd_loc = NERD(csv_loc, ['LOCATION'])
            nerd_time = NERD(csv_time, ['DATE', 'TIME'])

            extractor = FiveWExtractor(preprocessor, [nerd_loc, nerd_time])
            documents = gate_reader.parse_dir(document_path)
            for document in documents:
                log.info('Parsing %s' % document.get_title()[:50])
                extractor.parse(document)
