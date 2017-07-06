import json
import logging
import math
import os
import queue
import sys
from threading import Thread

from extractor.extractor import FiveWExtractor
from extractor.tools.file.handler import Handler
from extractor.tools.util import cmp_text

# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
# from timeit import default_timer as timer


core_nlp_host = 'http://localhost:9000'


class Worker(Thread):
    def __init__(self, queue):
        ''' Constructor. '''
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            extractor, document = self._queue.get()
            if extractor and document:
                extractor._evaluate_candidates(document)
                self._queue.task_done()


def adjustWeights(extractors, i, j, k, l):
    # (action_0, cause_1, environment_2)
    extractors[0].weights = (i, j, k)
    ## time
    extractors[1].weights = ((i, j), (i, j, k, l))
    ## cause - (position, conjunction, adverb, verb)
    extractors[2].weights = (i, j, k, l)


def cmp_text_helper(question, answers, annotations, weights, document, resultObjects):
    score = -1
    if question in annotation and question in answers:
        topAnswer = answers[question][0].get_parts()
        topAnnotation = annotation[question][0][2]
        score = cmp_text(topAnnotation, topAnswer)
    resultObjects[question].append({'weights': weights, 'score': score, 'document_id': document.get_document_id()})


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    # Setup
    extractorObject = FiveWExtractor()
    inputPath = os.path.dirname(__file__) + '/input/'
    preprocessedPath = os.path.dirname(__file__) + '/cache'

    increment_range = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                       0.85, 0.90, 0.95, 1]
    # increment_range = [0.10, 0.15, 0.45, 0.50, 0.55, 1]
    questions = {'when', 'why', 'who', 'how', 'what'}

    increment_range_length = len(increment_range)
    increment_range_steps = math.pow(increment_range_length, 4) / 100

    q = queue.Queue()
    resultFiles = {}
    resultObjects = {}

    for i in range(8):
        t = Worker(q)
        t.daemon = True
        t.start()

    # Put all together, run it once, get the cached document objects
    documents = (
        # initiate the newsplease file handler with the input directory
        Handler(inputPath)
            # set a path to save an load preprocessed documents
            .set_preprocessed_path(preprocessedPath)
            # limit the the to process documents (nice for development)
            .set_limit(1)
            # add an optional extractor (it would do basically just copying without...)
            .set_extractor(extractorObject)
            # saves all document objects for further programming
            .preload_and_cache_documents()
            # executing it
            .process().get_documents()
    )

    resultPath = os.path.dirname(__file__) + '/result/learnWeights'

    for question in questions:
        resultFiles[question] = open(resultPath + '_' + str(question) + '.json', encoding='utf-8', mode='w')
    for question in questions:
        resultObjects[question] = []

        # with open(resultPath, encoding='utf-8', mode='r') as data_file:
        # data = json.load(data_file)

    # grab utilities to parse dates and locations from the EnvironmentExtractor
    geocoder = extractorObject.extractors[1].geocoder
    calendar = extractorObject.extractors[1].calendar

    # Questions

    for document in documents:
        # manually generate candidate lists
        # candidates = [e._extract_candidates(document) for e in extractor.extractors]

        counter = 0
        print("Progress: " + str(counter / increment_range_steps) + "%", end="\r")
        # try all weight combinations
        for i in increment_range:
            for j in increment_range:
                for k in increment_range:
                    for l in increment_range:

                        adjustWeights(extractorObject.extractors, i, j, k, l)

                        # 2__Reevaluate per extractor
                        for extractor in extractorObject.extractors:
                            q.put((extractor, document))

                        q.join()

                        # for extractor in extractorObject.extractors:
                        #   extractor._evaluate_candidates(document)

                        # 2_1 Reevaluate combined scoring
                        for combinedScorer in extractorObject.combinedScorers:
                            combinedScorer.score(document)

                        annotation = document.get_annotations()
                        answers = document.get_answers()

                        cmp_text_helper('why', answers, annotation, [i, j, k, l], document, resultObjects)
                        cmp_text_helper('what', answers, annotation, [i, j, k], document, resultObjects)
                        cmp_text_helper('who', answers, annotation, [i, j, k], document, resultObjects)
                        cmp_text_helper('how', answers, annotation, [i, j], document, resultObjects)

                        #
                        # cmp_text_helper('when', answers, annotation, [i, j, k, l], document, resultObjects)
                        counter = counter + 1
                print("Progress: " + str(counter / increment_range_steps) + " %")

    # save everything
    for question in questions:
        # order: the result
        resultObjects[question].sort(key=lambda x: x['score'], reverse=True)

        # write to the disk
        resultFiles[question].write(
            json.dumps(resultObjects[question], sort_keys=False, indent=2, check_circular=False))
        resultFiles[question].close()


#
# result = {
#     'when': {
#         'weights':[i, j, k, l],
#         'score': when
#     },
#     'why': {
#         'weights':{
#              'position': i,
#              'conjunction': j,
#              'adverb': k,
#              'verb': l
#         },
#         'score': why
#     },
#     'who': {
#         'weights':{
#              'position': i,
#              'frequency': j,
#              'namedEntity': k
#         },
#         'score': who
#     },
#     'what': {
#         'weights':{
#              'position': i,
#              'frequency': j,
#              'namedEntity': k
#         },
#         'score': what
#     },
#     'how': {
#         'weights':{
#              'position': i,
#              'frequency': j
#         },
#         'score': how
#     }
# }
