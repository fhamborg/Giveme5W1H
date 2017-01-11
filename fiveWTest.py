import logging
import os
import csv
import gateReader
from preprocessor import Preprocessor
from fiveWExtractor import FiveWExtractor
from extractors import actionExtractor, environmentExtractor, causeExtractor

# This is just a simple example how to use the extractor


def save_csv(csv_file, doc, n=3):
    # writes results and annotation to a csv file

    writer = csv.writer(csv_file)
    writer.writerow([document.raw_title])

    questions = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}

    # read gate annotations
    for annotation in [a for a in doc.annotations if a[0] == 'FiveW']:
        features = {'question': '-', 'id': '1', 'accuracy': '1'}

        for feature in annotation[1]:
            features[feature[0]] = feature[1]

        if features['question'] in questions.keys():
            questions[features['question']].append((features['id'], features['accuracy'], annotation[2]))

    # write to csv file
    for question in questions.keys():
        topn_annotations = sorted(questions[question], key=lambda q: q[1])[:n]
        topn_results = doc.questions[question][:n]

        writer.writerow([question, 'annotation', '(id | accuracy)', 'result', 'score'])
        if max(len(topn_annotations), len(topn_results)) == 0:
            writer.writerow([])

        for i in range(n):
            row = ['', '', '', '', '']
            data = False

            if len(topn_annotations) > i:
                row[1] = topn_annotations[i][2]
                row[2] = ('(%s| %s)' % (topn_annotations[i][0], topn_annotations[i][1]))
                data = True

            if len(topn_results) > i:
                if question in ['where', 'why']:
                    answer = ' '.join(topn_results[i][0])
                else:
                    answer = ' '.join([token[0] for token in topn_results[i][0]])  # filter pos
                row[3] = answer
                row[4] = topn_results[i][1]
                data = True

            if data:
                writer.writerow(row)
    writer.writerow([])
    writer.writerow([])


if __name__ == '__main__':
    log = logging.Logger('FiveWTest')
    log.setLevel(20)

    # preprocessor expects the location of the sanford-ner.jar and a model to train the ner-parser
    # stanford-ner can be found here: http://nlp.stanford.edu/software/CRF-NER.shtml
    prep = Preprocessor('./data/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
                        './data/stanford-ner-2015-12-09/stanford-ner.jar')

    # initialize desired extractors
    extractor_list = [
        actionExtractor.ActionExtractor(),
        environmentExtractor.EnvironmentExtractor(),
        causeExtractor.CauseExtractor()
    ]

    extractor = FiveWExtractor(prep, extractor_list)
    documents = gateReader.parse_dir('./data/articles')

    n = 200

    with open('./results.csv', 'w') as file:
        for document in documents:
            if len(document.annotations) > 0:
                print('Parsing %s' % document.raw_title)
                extractor.parse(document)
                save_csv(file, document)

                n -= 1
                if n == 0:
                    break
