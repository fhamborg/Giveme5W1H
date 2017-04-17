import logging
import os
import json
import time
from timeit import default_timer as timer
from extractor.document import DocumentFactory
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.tools import gate_reader
from geopy.distance import vincenty
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from itertools import product

"""
This is a simple example on how to use the extractor in combination with our GATE reader.
This script extracts the five W answers from the text and creates csv to compare the results with the GATE annotations.

Please update the CoreNLP address to math your host.
"""

# path to dir with documents
d_path = '/home/soeren/PycharmProjects/Giveme5W/examples/sample_articles/annotation'
# path to dir with annotations
a_path = '/home/soeren/PycharmProjects/Giveme5W/examples/sample_articles/article'

# Host of the CoreNLP server
# For information on how to build/run a CoreNLP instance go to: https://stanfordnlp.github.io/CoreNLP/
core_nlp_host = 'http://132.230.224.141:9000'

# Increments
increment = 0.1

log = logging.getLogger('GiveMe5W')
log.setLevel(logging.INFO)

geocoder = None
calendar = None


def load_documents(d_path, a_path):
    documents = []
    factory = DocumentFactory()

    if not os.path.exists(d_path):
        log.warning('The given path does not exist: %s' % d_path)
    elif os.path.exists(a_path):
        log.warning('The given path does not exist: %s' % a_path)
    else:
        for root, directory, files in os.walk(d_path):
            for file in files:
                doc = gate_reader.parse_file(os.path.join(root, file), factory)

                if doc is not None:
                    # fetch annotation
                    with open(root.replace(d_path, a_path) + file) as annotation:
                        data = json.load(annotation)
                        doc.set_annotations(data['annotation'])

                    documents.append(doc)

    log.info('%i document and annotations loaded' % len(documents))

    return documents


def cmp_text(annotation, candidate):
    if annotation is None:
        return -1
    elif candidate is None:
        return -2

    # fetch synsets
    syn_a = [wordnet.synsets(t) for t in word_tokenize(annotation)]
    syn_b = [wordnet.synsets(t[0]) for t in candidate]

    # drop tokens without synsets
    syn_a = [syn for syn in syn_a if len(syn) > 0]
    syn_b = [syn for syn in syn_b if len(syn) > 0]

    if not any(syn_a) or not any(syn_b):
        # no synsets were found for one set!
        return -3

    score = 0
    max_b = [0] * len(syn_b)

    for i in range(len(syn_a)):
        max_a = 0
        for j in range(len(syn_b)):
            sim = max(list((wordnet.path_similarity(a, b) or 0) for a, b in product(syn_a[i], syn_b[j])) or [0])
            max_a = max(sim, max_a)
            max_b[j] = max(max_b[j], sim)

        score += max_a
    score += sum(max_b)

    return score / len(syn_a) + len(syn_b)


def cmp_date(annotation, candidate):
    if annotation is None:
        return -1
    elif candidate is None:
        return -2

    c_time = calendar.parse(candidate)

    # one of the answers couldn't be parsed
    if c_time[1] == 0:
        return -3

    return abs(time.mktime(annotation[0]) - time.mktime(c_time[0]))


def cmp_location(annotation, candidate):
    if annotation is None:
        return -1
    elif candidate is None:
        return -2

    location = geocoder.geocode(candidate)
    if location is None:
        return -3

    return vincenty(annotation.point, location.point)

if __name__ == '__main__':

    # init preprocessor and extractors manually
    preprocessor = Preprocessor(core_nlp_host)
    extractors = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]

    geocoder = extractors[1].geocoder
    calendar = extractors[1].calendar

    # load documents and annotation
    documents = load_documents(d_path, a_path)

    # generate result files
    files = {
        'action': open(os.path.expanduser('~') + '/who-matrix.csv', 'w+'),
        'when': open(os.path.expanduser('~') + '/when-matrix.csv', 'w+'),
        'where': open(os.path.expanduser('~') + '/where-matrix.csv', 'w+'),
        'why': open(os.path.expanduser('~') + '/why-matrix.csv', 'w+')
    }

    # write caption
    files['action'].write('position, frequency, named entity, score who, score what\n')
    files['when'].write('position, date, frequency, score\n')
    files['where'].write('position, frequency, score\n')
    files['why'].write('position, pattern type, score\n')

    start_all = timer()
    for document in documents:
        start = timer()

        # load (most important) annotation
        annotation = document.get_annotations()
        for question in annotation:
            if annotation[0] == 'NULL':
                annotation[question] = None
            elif question == 'when':
                time = calendar.parse(annotation[0])
                if time[1] == 0:
                    time = None
                annotation[question] = time
            elif question == 'where':
                annotation[question] = geocoder.geocode(annotation[0])
            else:
                annotation[question] = annotation[0]

        # manually generate candidate lists
        candidates = [e._extract_candidates(document) for e in extractors]

        # iterate through all possible weight constellations and record distance to annotation
        weights = [0, 0, 0]
        while weights[0] <= 1:
            while weights[1] <= 1:
                while weights[2] <= 1:
                    # action extractor - (position, frequency, named entity)
                    extractors[0].weights = weights
                    best = (extractors[0]._evaluate_candidates(document, candidates[0]) or [[None, None]])[0]
                    files['action'].write(("%f,%f,%f," % tuple(weights)) +
                                          str(cmp_text(annotation['who'], best[0])) + ',' +
                                          str(cmp_text(annotation['what'], best[1])) + '\n')

                    # environment extractor - ((position, frequency), (position, date, time, frequency))
                    extractors[1].weights = (weights[:2], (weights[0], 1-weights[1], weights[1], weights[2]))

                    # time
                    best = (extractors[1]._evaluate_dates(document, candidates[1][1]) or [[None]])[0][0]
                    files['when'].write(("%f,%f,%f," % tuple(weights)) + str(cmp_date(annotation['when'], best)) + '\n')

                    weights[2] += increment

                # location
                best = (extractors[1]._evaluate_locations(document, candidates[1][0]) or [[None]])[0][0]
                files['where'].write(("%f,%f," % tuple(weights[:2])) +
                                     str(cmp_location(annotation['where'], best)) + '\n')

                # cause extractor - (position, pattern type)
                extractors[2].weights = weights[:2]
                best = (extractors[2]._evaluate_candidates(document, candidates[2]) or [[None]])[0][0]
                files['why'].write(("%f,%f," % tuple(weights[:2])) + str(cmp_text(annotation['why'], best))
                                   + '\n')

                weights[1] += increment
            weights[0] += increment

            log.info("document parsed in %i" % (start - timer()))

    for file in files:
        files[file].close()

    diff_all = timer() - start_all
    log.info("total time={}, time/article={}".format(round(diff_all, 2), round(diff_all / len(documents), 2)))
