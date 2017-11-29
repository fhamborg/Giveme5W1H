import json
import logging
import math
import os
import pickle
import queue
import socket
import datetime
import sys
from threading import Thread
from dateutil.relativedelta import relativedelta as rd


import time

from combined_scoring import distance_of_candidate
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

fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'


def loadDocumentsAndCoder(extractors, combined_scorer):
    inputPath = path('../examples/datasets/gold_standard/data')
    preprocessedPath = path('../examples/datasets/gold_standard/cache')

    # Setup
    extractor_object = FiveWExtractor( extractors=list(extractors.values()), combined_scorers=[combined_scorer])

    # Put all together, run it once, get the cached document objects
    docments = (
        # initiate the newsplease file handler with the input directory
        Handler(inputPath)
            # set a path to save an load preprocessed documents
            .set_preprocessed_path(preprocessedPath)
            # limit the the to process documents (nice for development)
            .set_limit(50)
            # add an optional extractor (it would do basically just copying without...)
            .set_extractor(extractor_object)
            # saves all document objects for further programming
            .preload_and_cache_documents()
            # executing it
            .process().get_documents()
    )

    return docments, extractor_object



def cmp_text_helper(question, answers, annotations, weights, result):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers and len(annotations[question]) > 0  and len(answers[question]) > 0:
        topAnswer = answers[question][0].get_parts_as_text()
        for annotation in annotations[question]:
            if len(annotation) > 2:
                topAnnotation = annotation[2]
                if topAnnotation and topAnswer:
                    tmp_score = cmp_text(topAnnotation, topAnswer)
                    score = max(tmp_score, score)
    result[question] = (question, weights, score)


def cmp_date_helper(question, answers, annotations, weights, calendar, result):
    score = -1
    # check if there is an annotaton and an answer
    if question in annotations and question in answers and len(annotations[question]) > 0  and len(answers[question]) > 0:
        topAnswer = answers[question][0].get_parts_as_text()
        for annotation in annotations[question]:
            if len(annotation) > 2:
                topAnnotation = annotation[2]
                if topAnnotation and topAnswer:
                    tmp_score = cmp_date(topAnnotation, topAnswer, calendar)
                    score = max(tmp_score, score)

    result[question] = (question, weights, score)

def cmp_location_helper(question, answers, annotations, weights, geocoder, result):
    score = -1
    # check if there is an annotaton and answer
    if question in annotations and question in answers and len(annotations[question]) > 0 and len(answers[question]) > 0:
        topAnswer = answers[question][0].get_parts_as_text()
        for annotation in annotations[question]:
            if len(annotation) > 2:
                topAnnotation = annotation[2]
                if topAnnotation and topAnswer:
                    tmp_score = cmp_location(topAnnotation, topAnswer, geocoder)
                    score = max(tmp_score, score)
    result[question] = (question, weights, score)


def log_progress(queue,documents, start, end):
    count = queue.get_queue_count()
    doc_count = len(documents)
    print('There are ' + str(count * doc_count) + ' steps to go')
    if (start and end):
        time_range = (end - start).total_seconds()
        time_range = time_range * count
        # No proper average this is very rough


        print('Rough estimated time left:' + str( fmt.format(rd(seconds=time_range))))


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

    extractors = {
        'action': action_extractor.ActionExtractor(),
        'environment': environment_extractor.EnvironmentExtractor(),
        'cause': cause_extractor.CauseExtractor(),
        'method': method_extractor.MethodExtractor()
    }
    combined_scorer = distance_of_candidate.DistanceOfCandidate(('what', 'who'), ('how'))

    documents, extractor_object = loadDocumentsAndCoder(extractors, combined_scorer)

    # grab utilities to parse dates and locations from the EnvironmentExtractor
    if extractors.get('environment'):
        geocoder = extractors.get('environment').geocoder
        calendar = extractors.get('environment').calendar

    log_progress(queue,documents, None, None)
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

            if extractors.get('action'):
                #
                extractors['action'].weights = (i, j, k)

            if extractors.get('environment'):
                # time
                extractors['environment'].weights = ((i, j), (i, j, k, l))

            if extractors.get('cause'):
                # cause - (position, conjunction, adverb, verb)
                extractors['cause'].weights = (i, j, k, l)

            if extractors.get('method'):
                # method - (position, frequency)
                extractors['method'].weights = (i, j)


            combination_start_stamp =  datetime.datetime.now()
            # run for all documents
            for document in documents:

                try:
                    extractor_object.parse(document)
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

                cmp_date_helper('when', answers, annotation, [i, j, k, l], calendar, result)

                #try:
                    # cmp_location_helper('where', answers, annotation, [i, j], geocoder, result)
                #except socket.timeout:
                    #print('online service (prob nominatim) did`t work, we ignore this')


                # done save it to the result
                queue.resolve_document(next_item,  document.get_document_id(), result)

            combination_end_stamp = datetime.datetime.now()
            queue.pop(persist=True)
            log_progress(queue, documents, combination_start_stamp, combination_end_stamp)
        else:
            print('done')
            break
