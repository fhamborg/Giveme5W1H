import logging
import json
import time
from timeit import default_timer as timer
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from extractor.document import DocumentFactory
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.tools import gate_reader
from geopy.distance import vincenty
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from itertools import product
import json
import codecs

"""
This tool extracts all candidates from the given sample articles, iterates over a range of parameter increments and
compares the results with given annotations. The results are saved to .csv file.

!It is recommended run the question 'where' separate as a lost server-connection cancels all calculations!
"""

abs_path = '/'.join(os.path.realpath(__file__).split('/')[:-3])
# path to dir with documents
d_path = abs_path + '/examples/sample_articles/'
# path to .json file with annotations
a_path = abs_path + '/examples/sample_articles/golden.pjson'

# Host of the CoreNLP server
# For information on how to build/run a CoreNLP instance go to: https://stanfordnlp.github.io/CoreNLP/
core_nlp_host = 'localhost:9000'

# Increments
increment_range = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                   0.85, 0.90, 0.95, 1]

log = logging.getLogger('GiveMe5W')
log.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
log.addHandler(sh)

geocoder = None
calendar = None


def load_documents(d_path, a_path):
    """
    Loads the documents alongside the annotations and returns Document objects.

    :param d_path: Path to folder containing the gate files.
    :type d_path: String
    :param a_path: Path to .json file containing the annotations.
    :type a_path: String

    :return: [Document]
    """

    documents = []
    factory = DocumentFactory()

    if not os.path.exists(d_path):
        log.warning('The given path does not exist: %s' % d_path)
    elif not os.path.isfile(a_path):
        log.warning('The given file does not exist: %s' % a_path)
    else:
        # load annotations
        with codecs.open(a_path, 'r', 'utf-8-sig') as file:
            #annotations = json.load(file)
            # just open the file...
            
            # need to use codecs for output to avoid error in json.dump
            #output_file = codecs.open("output_file.json", "w", encoding="utf-8")
            
            # read the file and decode possible UTF-8 signature at the beginning
            # which can be the case in some files.
            annotations = json.load(file)

        for root, directory, files in os.walk(d_path):
            for file in files:
                doc = gate_reader.parse_file(os.path.join(root, file), factory)
                
                if doc is not None:
                    print(doc.get_annotations())
                    # fetch annotation
                    annotation = {}
                    for question in annotations[file]:
                        annotation[question] = annotations[file][question][0][0]
                        doc.set_annotations(annotation)
                        # store filename in 'what'-field
                        doc.set_answer('what', file)
                    print(annotation)
                    documents.append(doc)

    log.info('%i document and annotations loaded' % len(documents))

    return documents


def cmp_text(annotation, candidate):
    """
    Compare the retrieved answer with the annotation using WordNet path distance.

    :param annotation: The correct Answer
    :type annotation: String
    :param candidate: The retrieved Answer
    :type candidate: [String, String]

    :return: Float
    """

    if annotation is None:
        # annotation is NULL
        return -1
    elif candidate is None:
        # no answer was extracted
        return -2

    # fetch synsets for both answers
    syn_a = [wordnet.synsets(t) for t in word_tokenize(annotation)]
    syn_b = [wordnet.synsets(t[0]) for t in candidate]

    # drop tokens without synsets
    syn_a = [syn for syn in syn_a if len(syn) > 0]
    syn_b = [syn for syn in syn_b if len(syn) > 0]

    if not any(syn_a) or not any(syn_b):
        # no synsets were found for one of the answers!
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
    """
    Compare the retrieved answer with the annotation by calculating the time difference in seconds.

    :param annotation: The correct Answer
    :type annotation: (time.struct_time, Integer)
    :param candidate: The retrieved Answer
    :type candidate: [String]

    :return: Float
    """

    if annotation is None:
        # annotation is NULL
        return -1
    elif candidate is None:
        # no answer was extracted
        return -2

    c_time = calendar.parse(' '.join(candidate))

    if c_time[1] == 0:
        # one of the answers couldn't be parsed
        return -3

    return abs(time.mktime(annotation[0]) - time.mktime(c_time[0]))


def cmp_location(annotation, candidate):
    """
    Compare the retrieved answer with the annotation using geocoding and comparing the real world distance.

    :param annotation: The geocoded correct Answer
    :type annotation: Location
    :param candidate: The retrieved Answer
    :type candidate: Sting

    :return: Float
    """

    if annotation is None:
        # annotation is NULL or the annotation could'nt be parsed
        return -1
    elif candidate is None:
        # no answer was extracted
        return -2

    location = geocoder.geocode(candidate)
    if location is None:
        # retrieved answer couldn't be parsed
        return -3

    return vincenty(annotation.point, location.point).kilometers

if __name__ == '__main__':

    # init preprocessor and extractors manually
    preprocessor = Preprocessor(core_nlp_host)
    extractors = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]

    # grab utilities to parse dates and locations from the EnvironmentExtractor
    geocoder = extractors[1].geocoder
    calendar = extractors[1].calendar

    # load documents and annotation
    start = timer()
    documents = load_documents(d_path, a_path)
    for document in documents:
        preprocessor.preprocess(document)
        print(document.get_answers()['what'])
    log.info('Document preprocessed in %i' % (timer() - start))

    start_all = timer()

    for document in documents:
        start = timer()
        prefix = document.get_answers()['what'][:-4]

        # generate result files
        files = {
            'action': open(os.path.expanduser('~') + '/confusion/who-matrix_' + prefix + '.csv', 'w+'),
            'when': open(os.path.expanduser('~') + '/confusion/when-matrix_' + prefix + '.csv', 'w+'),
            'why': open(os.path.expanduser('~') + '/confusion/why-matrix_' + prefix + '.csv', 'w+')
        }

        # write caption
        files['action'].write('position,frequency,named entity,score who,score what\n')
        files['when'].write('position,date,frequency,score\n')
        files['why'].write('position,conjunction,adverb,verb,score\n')

        # load (most important) annotation
        annotation = document.get_annotations()
        for question in annotation:
            if annotation[question] == 'NULL':
                annotation[question] = None
            elif question == 'when':
                t = calendar.parse(annotation[question])
                if t[1] == 0:
                    t = None
                annotation[question] = t
            elif question == 'where':
                annotation[question] = geocoder.geocode(annotation[question])

        # manually generate candidate lists
        candidates = [e._extract_candidates(document) for e in extractors]

        # iterate through all possible parameter constellations and record distance to annotation
        for i in increment_range:
            for j in increment_range:
                for k in increment_range:
                    for l in increment_range:
                        # environment extractor - ((position, frequency), (position, date, time, frequency))
                        extractors[1].weights = ((i, j), (i, j, k, l))

                        # time
                        best = (extractors[1]._evaluate_dates(document, candidates[1][1]) or [[None]])[0][0]
                        files['when'].write(
                            ("%f,%f,%f,%f," % (i, j, k, l)) + str(cmp_date(annotation['when'], best)) + '\n')

                        # cause extractor - (position, conjunction, adverb, verb)
                        extractors[2].weights = (i, j, k, l)
                        best = (extractors[2]._evaluate_candidates(document, candidates[2]) or [[None]])[0][0]
                        files['why'].write(("%f,%f,%f,%f," % (i, j, k, l)) + str(cmp_text(annotation['why'], best))
                                           + '\n')

                    # action extractor - (position, frequency, named entity)
                    extractors[0].weights = (i, j, k)
                    best = (extractors[0]._evaluate_candidates(document, candidates[0]) or [[None, None]])[0]
                    files['action'].write(("%f,%f,%f," % (i, j, k)) +
                                          str(cmp_text(annotation['who'], best[0])) + ',' +
                                          str(cmp_text(annotation['what'], best[1])) + '\n')

        log.info("document parsed in %i" % (timer() - start))

        for file in files:
            files[file].close()

    diff_all = timer() - start_all
    log.info("total time={}, time/article={}".format(round(diff_all, 2), round(diff_all / len(documents), 2)))
