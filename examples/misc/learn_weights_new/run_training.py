"""
Helper to run learn with different configurations.
Be sure to remove the training set from input before running
"""
import logging
import queue
import threading

from combined_scoring import distance_of_candidate
from extractor.root import path
from extractors import environment_extractor, action_extractor, cause_extractor, method_extractor
from misc.learn_weights_new.learn import Learn, Worker
from misc.learn_weights_new.work_queue import WorkQueue

inputPath = path('../examples/datasets/gold_standard/data')
preprocessedPath = path('../examples/datasets/gold_standard/cache')


def method(lock):
    a_queue = WorkQueue(id='training', generator='method')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'method': method_extractor.MethodExtractor()
    }
    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='training',
                  combined_scorer=None, queue=a_queue)
    return learn


def cause(lock):
    a_queue = WorkQueue(id='training', generator='cause')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'cause': cause_extractor.CauseExtractor()
    }

    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='training',
                  combined_scorer=None, queue=a_queue)
    return learn


def environment(lock):
    a_queue = WorkQueue(id='training', generator='environment')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'environment': environment_extractor.EnvironmentExtractor()
    }

    learn = Learn(lock=lock, extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def action(lock):
    a_queue = WorkQueue(id='training', generator='action')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
         'action': action_extractor.ActionExtractor()
        # 'environment': environment_extractor.EnvironmentExtractor(),
        # 'cause': cause_extractor.CauseExtractor(),
        # 'method': method_extractor.MethodExtractor()
    }
    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='training',
                  combined_scorer=None, queue=a_queue)
    return learn


def default_combined_scoring(lock):
    a_queue = WorkQueue(id='training_cs', generator='method')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'method': method_extractor.MethodExtractor(),
        'action': action_extractor.ActionExtractor()  # provider for what an who
    }
    # set optimal weights learned beforehand
    extractors['action'].weights = [0.7, 0.3, 0.9]

    combined_scorer = distance_of_candidate.DistanceOfCandidate(['what'], 'how')

    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='training',
                  combined_scorer=combined_scorer,
                  queue=a_queue,
                  ignore_extractor=['action'])
    return learn


if __name__ == '__main__':

    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    log.addHandler(sh)

    # basic learner
    # log.setLevel(logging.ERROR)

    # thread safe queue
    q = queue.Queue()
    lock = threading.Lock()  # Wordnet is not threadsave


    q.put(action(lock))
    #weights = [[]]
    #q.put(environment(lock, weights))
    q.put(cause(lock))
    q.put(method(lock))



    for i in range(4):
        t = Worker(q)
        t.daemon = True
        t.start()

    # wait till all extractors are done
    q.join()
