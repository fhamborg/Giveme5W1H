import json
import logging
import math
import os
import pickle
import queue
import sys
from threading import Thread

from extractor.extractor import FiveWExtractor
from extractor.tools.file.handler import Handler
from extractor.tools.util import cmp_text, cmp_date, cmp_location

# Add path to allow execution though console
#sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
# from timeit import default_timer as timer


core_nlp_host = 'http://localhost:9000'


class Worker(Thread):
    """
    Thread helper
    """

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


class WeightQueue:
    _documentIndex = 0
    _weight_queue_index = 0

    _tmp_counter = 0
    _counter = 0
    _document_counter = 0

    def __init__(self, increment_range, save_interval=30, ):

        self._documents, self._geocoder, self._calendar, self._extractor = loadDocumentsAndCoder()

        self._document_counter = len(self._documents)

        self._increment_range_length = len(increment_range)
        # interval has 4 dimensions
        self._increment_range_steps = math.pow(self._increment_range_length, 4) / 100
        # each document is going through the interval once
        self._increment_range_steps = self._increment_range_steps * self._document_counter

        # save each n-th step
        self._save_interval = save_interval
        self.create_new_interval_queue()

    def create_new_interval_queue(self):
        self._weight_queue = []
        for i in increment_range:
            for j in increment_range:
                for k in increment_range:
                    for l in increment_range:
                        self._weight_queue.append((i, j, k, l))

    def next(self, ):
        # return document
        return self._weight_queue.pop(), self._documents[self._document_counter - 1]

    def has_next(self, file_handler):
        # helper to get every n-th item a progress indicator
        # saves also the current state, before poping the next item
        if self._tmp_counter > self._save_interval:
            print("Progress: " + str(self._counter / self._increment_range_steps) + " %")
            file_handler.save()
            print("saved")
            self._tmp_counter = 0
        else:
            self._tmp_counter += 1

        self._counter += 1

        if len(self._weight_queue) > 0:
            return True
        else:
            if self._document_counter > 0:
                # process the next document
                self.create_new_interval_queue()
                self._document_counter -= 1
            else:
                # done
                return False


class FileHandler:
    _resultFiles = {}
    _resultObjects = {}
    _questions = None
    _weight_queue = None

    def __init__(self, questions, resultPath, weightQueuePath):
        self._questions = questions
        self._weightQueuePath = weightQueuePath

        for question in self._questions:
            self._resultFiles[question] = open(resultPath + '_' + str(question) + '.json', encoding='utf-8', mode='w')
            try:
                self._resultObjects[question] = json.load(self._resultFiles[question])
                break
            except OSError as err:
                # initial call create an array
                self._resultObjects[question] = []

    def add_result(self, question, weights, score, document_id):
        self._resultObjects[question].append({'weights': weights, 'score': score, 'document_id': document_id})

    def get_weight_queue(self):

        if not self._weight_queue:
            if os.path.isfile(self._weightQueuePath):
                # _preprocessedPath path is given, and there is already a preprocessed document
                with open(self._weightQueuePath, 'rb') as ff:
                    print("weightQueue instance found! continue processing :)")
                    self._weight_queue = pickle.load(ff)
            else:
                self._weight_queue = WeightQueue(increment_range)
        return self._weight_queue;

    def save(self):
        for question in self._questions:
            # order: the result
            self._resultObjects[question].sort(key=lambda x: x['score'], reverse=True)

            # write to disk
            self._resultFiles[question].write(
                json.dumps(self._resultObjects[question], sort_keys=False, indent=2, check_circular=False))

            # save the questate for this data state
            # with open(self._weightQueuePath, 'wb') as f:
            # Pickle the 'data' document using the highest protocol available.
            #   pickle.dump(self._weight_queue, f, pickle.HIGHEST_PROTOCOL)

    def closeAndRemoveWeightQueue(self):
        os.remove(self._weightQueuePath, dir_fd=None)
        for question in self._questions:
            self._resultFiles[question].close()


def adjust_weights(extractors, i, j, k, l):
    # (action_0, cause_1, environment_2)
    extractors[0].weights = (i, j, k)
    # time
    extractors[1].weights = ((i, j), (i, j, k, l))
    # cause - (position, conjunction, adverb, verb)
    extractors[2].weights = (i, j, k, l)
    # method - (position, frequency)
    extractors[3].weights = (i, j)


def cmp_text_helper(question, answers, annotations, weights, document, fileHandler):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers:
        topAnswer = answers[question][0].get_parts()
        topAnnotation = annotations[question][0][2]
        score = cmp_text(topAnnotation, topAnswer)

    fileHandler.add_result(question, weights, score, document.get_document_id())


def cmp_date_helper(question, answers, annotations, weights, document, fileHandler):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers:
        topAnswer = answers[question][0][0]
        topAnnotation = annotations[question][0][2]
        score = cmp_date(topAnnotation, topAnswer, fileHandler.get_weight_queue()._calendar)

    fileHandler.add_result(question, weights, score, document.get_document_id())


def cmp_location_helper(question, answers, annotations, weights, document, fileHandler):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers:
        topAnswer = answers[question][0][0]
        topAnnotation = annotations[question][0][2]
        score = cmp_location(topAnnotation, topAnswer, fileHandler.get_weight_queue()._geocoder)

    fileHandler.add_result(question, weights, score, document.get_document_id())


def loadDocumentsAndCoder():
    # Setup
    extractorObject = FiveWExtractor()
    inputPath = os.path.dirname(__file__) + '/input/'
    preprocessedPath = os.path.dirname(__file__) + '/cache'
    # Put all together, run it once, get the cached document objects
    docments = (
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

    # grab utilities to parse dates and locations from the EnvironmentExtractor
    geocoder = extractorObject.extractors[1].geocoder
    calendar = extractorObject.extractors[1].calendar

    return docments, geocoder, calendar, extractorObject


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    increment_range = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                       0.85, 0.90, 0.95, 1]
    # increment_range = [0.10, 0.15, 1]
    questions = {'when', 'why', 'who', 'how', 'what', 'where'}

    resultPath = os.path.dirname(__file__) + '/result/learnWeights'
    weightQueuePath = os.path.dirname(__file__) + '/result/weightQueue.prickle'

    fileHandler = FileHandler(questions, resultPath, weightQueuePath)
    weightQueue = fileHandler.get_weight_queue()
    extractorObject = weightQueue._extractor
    q = queue.Queue()

    for i in range(5):
        t = Worker(q)
        t.daemon = True
        t.start()

        # Questions
        # for document in documents:
        while weightQueue.has_next(fileHandler):
            weights, document = weightQueue.next()

            i = weights[0]
            j = weights[1]
            k = weights[2]
            l = weights[3]
            adjust_weights(extractorObject.extractors, i, j, k, l)

            # 2__Reevaluate per extractor
            for extractor in extractorObject.extractors:
                q.put((extractor, document))
            q.join()

            # 2_1 Reevaluate, combined scoring
            for combinedScorer in extractorObject.combinedScorers:
                combinedScorer.score(document)

            annotation = document.get_annotations()
            answers = document.get_answers()

            cmp_text_helper('why', answers, annotation, [i, j, k, l], document, fileHandler)
            cmp_text_helper('what', answers, annotation, [i, j, k], document, fileHandler)
            cmp_text_helper('who', answers, annotation, [i, j, k], document, fileHandler)
            cmp_text_helper('how', answers, annotation, [i, j], document, fileHandler)

            # These two are tricky because of the used online services
            cmp_date_helper('when', answers, annotation, [i, j, k, l], document, fileHandler)
            cmp_location_helper('where', answers, annotation, [i, j], document, fileHandler)
            # counter = counter + 1

    print("Done")
    fileHandler.save()
    fileHandler.closeAndRemoveWeightQueue()
