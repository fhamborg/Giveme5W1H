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






            # done without any exceptions...remove item
            queue.pop()
        else:
            print('done')
            break


    # TODO generate some settings