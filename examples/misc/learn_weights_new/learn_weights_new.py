import json
import logging
import math
import os
import pickle
import queue
import socket
import sys
from threading import Thread

import time

from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler
from extractor.tools.util import cmp_text, cmp_date, cmp_location

# Add path to allow execution though console
# sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
# from timeit import default_timer as timer
# core_nlp_host = 'http://localhost:9000'
from extractors import environment_extractor, action_extractor, cause_extractor, method_extractor
from misc.learn_weights_new.work_queue import WorkQueue



def adjust_weights(extractors, i, j, k, l):
    # (action_0, cause_1, environment_2)
    extractors[0].weights = (i, j, k)
    # time
    extractors[1].weights = ((i, j), (i, j, k, l))
    # cause - (position, conjunction, adverb, verb)
    extractors[2].weights = (i, j, k, l)
    # method - (position, frequency)
    extractors[3].weights = (i, j)

def loadDocumentsAndCoder():


    #inputPath = os.path.dirname(__file__) + '../../input/'
    inputPath = path('../examples/datasets/gold_standard/data')
    preprocessedPath = path('../examples/datasets/gold_standard/cache')
    #preprocessedPath = os.path.dirname(__file__) + '/cache'

    # Setup
    extractorObject = FiveWExtractor()


    # Put all together, run it once, get the cached document objects
    docments = (
        # initiate the newsplease file handler with the input directory
        Handler(inputPath)
            # set a path to save an load preprocessed documents
            .set_preprocessed_path(preprocessedPath)
            # limit the the to process documents (nice for development)
            # .set_limit(1)
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


def cmp_text_helper(question, answers, annotations, weights, result):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers and len(annotations[question]) > 0  and len(answers[question]) > 0:
        topAnswer = answers[question][0].get_parts_as_text()
        topAnnotation = annotations[question][0][2]
        score = cmp_text(topAnnotation, topAnswer)

    result[question] = (question, weights, score)



def cmp_date_helper(question, answers, annotations, weights, calendar, result):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers and len(annotations[question]) > 0  and len(answers[question]) > 0:
        topAnswer = answers[question][0].get_parts_as_text()
        topAnnotation = annotations[question][0][2]
        score = cmp_date(topAnnotation, topAnswer, calendar)

    result[question] = (question, weights, score)


def cmp_location_helper(question, answers, annotations, weights, geocoder, result):
    score = -1
    # check if there is an annotaton and answer
    if question in annotations and question in answers and len(annotations[question]) > 0 and len(answers[question]) > 0:
        topAnswer = answers[question][0].get_parts_as_text()
        topAnnotation = annotations[question][0][2]
        score = cmp_location(topAnnotation, topAnswer, geocoder)

    result[question] = (question, weights, score)


def log_progress(queue,documents):
    count = queue.get_queue_count()
    print('There are ' + str(count * len(documents)) + ' steps to go')


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    log.addHandler(sh)

    queue = WorkQueue()
    queue.setup_scoring_parameters()
    queue.setup_extracting_parameters()
    queue.load()

    documents, geocoder, calendar, extractor = loadDocumentsAndCoder()

    log_progress(queue,documents)
    # make sure caller can read that...
    time.sleep(5)





    _pre_extracting_parameters_id = None
    while True:
        next_item = queue.next()
        if next_item is not None:
            if _pre_extracting_parameters_id:

                if _pre_extracting_parameters_id != next_item['extracting_parameters_id']:
                    print("reset candidates - extracting values changed")
                    for document in documents:
                        document.reset_candidates

            _pre_extracting_parameters_id = next_item['extracting_parameters_id']

            # adjust weights
            weights = next_item['scoring_parameters']['weights']
            i = weights[0]
            j = weights[1]
            k = weights[2]
            l = weights[3]
            adjust_weights(extractor.extractors, i, j, k, l)

            # run for all documents
            for document in documents:

                try:
                    extractor.parse(document)
                except socket.timeout:
                    print('online service (prob nominatim) did`t work, we ignore this')

                annotation = document.get_annotations()
                answers = document.get_answers()

                result = {}

                cmp_text_helper('why', answers, annotation, [i, j, k, l], result)
                cmp_text_helper('what', answers, annotation, [i, j, k], result)
                cmp_text_helper('who', answers, annotation, [i, j, k], result)
                cmp_text_helper('how', answers, annotation, [i, j], result)

                # These two are tricky because of the used online services
                try:
                    cmp_date_helper('when', answers, annotation, [i, j, k, l], calendar, result)
                except socket.timeout:
                    print('online service (prob nominatim) did`t work, we ignore this')
                cmp_location_helper('where', answers, annotation, [i, j], geocoder, result)

                # done save it to the result
                queue.resolve_document(next_item,  document.get_document_id(), result)


            queue.pop(persist=True)
            log_progress(queue, documents)
        else:
            print('done')
            break


    # TODO generate some settings