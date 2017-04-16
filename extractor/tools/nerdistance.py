import csv
import os
import logging
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractors.abs_extractor import AbsExtractor
from extractor.extractor import FiveWExtractor
from extractor.tools import gate_reader

"""
This extractor actually measures the distance between named entities of the same type.

"""

class NERD(AbsExtractor):
    def __init__(self, writer, tags=[]):
        self.pairs = []
        self.writer = writer
        self.tags = tags
        writer.writerow(tags)

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
                        self.writer.writerow([first[1], sentence[i][1], i - first[0],
                                             ' '.join([t[0] for t in sentence[first[0]:i+1]])])
                        first = (i, sentence[i][1])

        return  document

if __name__ == '__main__':

    log = logging.getLogger('GiveMe5W')

    # Host of the CoreNLP server
    # For information on how to build/run a CoreNLP instance go to: https://stanfordnlp.github.io/CoreNLP/
    core_nlp_host = 'http://132.230.224.141:9000'
    preprocessor = Preprocessor(core_nlp_host)

    with open(os.path.expanduser('~') + '/nerd_loc.csv', 'w') as csv_loc:
        with open(os.path.expanduser('~') + '/nerd_time.csv', 'w') as csv_time:
            writer_loc = csv.writer(csv_loc)
            writer_time = csv.writer(csv_time)

            # initialize NERD object for time and location
            nerd_loc = NERD(writer_loc, ['LOCATION'])
            nerd_time = NERD(writer_time, ['DATE', 'TIME'])

            extractor = FiveWExtractor(preprocessor, [nerd_loc, nerd_time])
            path = '/'.join(os.path.dirname(__file__).split('/')[:-2]) + '/examples/sample_articles'
            documents = gate_reader.parse_dir(path)
            for document in documents:
                log.info('Parsing %s' % document.get_title()[:50])
                extractor.parse(document)
