import json
import logging
import math
import os
import pickle
import queue
import sys
from threading import Thread

from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler
from extractor.tools.util import cmp_text, cmp_date, cmp_location

# Add path to allow execution though console
# sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
# from timeit import default_timer as timer
# core_nlp_host = 'http://localhost:9000'
from extractors import environment_extractor, action_extractor, cause_extractor, method_extractor
from misc.learn_weights_smart.work_queue import WorkQueue



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


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    queue = WorkQueue()
    queue.setup_scoring_parameters()
    queue.setup_extracting_parameters()
    queue.load()

    documents, geocoder, calendar, extractor = loadDocumentsAndCoder()

    _pre_extracting_parameters_id = None
    while True:
        next_item = queue.next()
        if next_item is not None:
            if _pre_extracting_parameters_id:

                if _pre_extracting_parameters_id != next_item['extracting_parameters_id']:
                    for document in documents:
                        document.reset_candidates
                    print("reset candidates - extracting values changed")

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
                extractor.parse(document)

                annotation = document.get_annotations()
                answers = document.get_answers()

                cmp_text_helper('why', answers, annotation, [i, j, k, l], document, fileHandler)
                cmp_text_helper('what', answers, annotation, [i, j, k], document, fileHandler)
                cmp_text_helper('who', answers, annotation, [i, j, k], document, fileHandler)
                cmp_text_helper('how', answers, annotation, [i, j], document, fileHandler)

                # These two are tricky because of the used online services
                cmp_date_helper('when', answers, annotation, [i, j, k, l], document, fileHandler)
                cmp_location_helper('where', answers, annotation, [i, j], document, fileHandler)





            # done without any exceptions...remove item
            queue.pop()
        else:
            print('done')
            break


    # TODO generate some settings