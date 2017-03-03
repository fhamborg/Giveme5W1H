import sys
import os
import csv

sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from extractor.extractors.abs_extractor import AbsExtractor
from extractor.five_w_extractor import FiveWExtractor
from extractor.tools import gate_reader



class NERD(AbsExtractor):
    def __init__(self, writer, tags=[]):
        self.pairs = []
        self.writer = writer
        self.tags = tags
        writer.writerow(tags)

    def extract(self, document):
        for sentence in document.nerTags:
            first = None
            for i in range(len(sentence)):
                if sentence[i][1] in self.tags:
                    if first is None:
                        first = (i, sentence[i][1])
                    else:
                        self.writer.writerow([first[1], sentence[i][1], i - first[0],
                                         ' '.join([t[0] for t in sentence[first[0]:i+1]])])
                        first = (i, sentence[i][1])

if __name__ == '__main__':
    path = '/'.join(os.path.realpath(__file__).split('/')[:-3])

    with open(path + '/data/nerd_loc.csv', 'w') as csv_loc:
        with open(path + '/data/nerd_time.csv', 'w') as csv_time:
            writer_loc = csv.writer(csv_loc)
            writer_time = csv.writer(csv_time)
            nerd_loc = NERD(writer_loc, ['LOCATION'])
            nerd_time = NERD(writer_time, ['DATE', 'TIME'])
            extractor = FiveWExtractor([nerd_loc, nerd_time])
            documents = gate_reader.parse_dir(path + '/data/articles')
            for document in documents:
                print('Parsing %s' % document.raw_title)
                extractor.parse(document)
