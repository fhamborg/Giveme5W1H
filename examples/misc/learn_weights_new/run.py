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
from extractors import environment_extractor, action_extractor, cause_extractor, method_extractor
from misc.learn_weights_new.learn import Learn
from misc.learn_weights_new.work_queue import WorkQueue

from combined_scoring import distance_of_candidate
from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler
from extractor.tools.util import cmp_text, cmp_date, cmp_location


class Worker(Thread):
    def __init__(self, queue):
        ''' Constructor. '''
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            _learn = self._queue.get()
            _learn.process()
            self._queue.task_done()

if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    log.addHandler(sh)

    # thread safe queue
    q = queue.Queue()

    # basic parameter
    inputPath = path('../examples/datasets/gold_standard/data')
    preprocessedPath = path('../examples/datasets/gold_standard/cache')

    queue = WorkQueue('action', generator=WorkQueue.generate_action)
    queue.setup_scoring_parameters()
    queue.setup_extracting_parameters()
    queue.load()

    extractors = {
         'action': action_extractor.ActionExtractor(),
         #'environment': environment_extractor.EnvironmentExtractor(),
         #'cause': cause_extractor.CauseExtractor(),
         #'method': method_extractor.MethodExtractor()
    }
    #combined_scorer = distance_of_candidate.DistanceOfCandidate(('what', 'who'), ('how'))
    combined_scorer = None

    learn = Learn(extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath, combined_scorer=combined_scorer, queue=queue)
    q.put(learn)

    # creating worker threads
    for i in range(1):
        t = Worker(q)
        t.daemon = True
        t.start()

    # wait till oll extractors are done
    q.join()