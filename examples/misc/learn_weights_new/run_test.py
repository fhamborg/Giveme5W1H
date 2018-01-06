"""
Helper to run learn with different configurations.
Be sure to remove the training set from input before running
"""
import json
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


def load_best_weights(path):
    with open(path, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return data['best_dist']['weights']


def method(lock, pre_calculated_weights):
    a_queue = WorkQueue(id='test_method', generator='pre_calculated', pre_calculated_weights=pre_calculated_weights)
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
                  sampling='test',
                  combined_scorer=None, queue=a_queue)
    return learn


def cause(lock, pre_calculated_weights):
    a_queue = WorkQueue(id='test_cause', generator='pre_calculated', pre_calculated_weights=pre_calculated_weights)
    a_queue.load()

    extractors = {
        'cause': cause_extractor.CauseExtractor()
    }

    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='test',
                  combined_scorer=None, queue=a_queue)
    return learn


def environment_where(lock, pre_calculated_weights):
    a_queue = WorkQueue(id='test_environment_where', generator='pre_calculated', pre_calculated_weights=pre_calculated_weights)

    a_queue.load()

    extractors = {
        'environment_where': environment_extractor.EnvironmentExtractor(skip_when=True)
    }

    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='test',
                  combined_scorer=None, queue=a_queue)
    return learn

def environment_when(lock, pre_calculated_weights):
    a_queue = WorkQueue(id='test_environment_when', generator='pre_calculated', pre_calculated_weights=pre_calculated_weights)

    a_queue.load()

    extractors = {
        'environment_when': environment_extractor.EnvironmentExtractor( skip_where=True)
    }

    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='test',
                  combined_scorer=None, queue=a_queue)
    return learn


def action(lock, pre_calculated_weights):
    a_queue = WorkQueue(id='test_action', generator='pre_calculated', pre_calculated_weights=pre_calculated_weights)
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
         'action': action_extractor.ActionExtractor()
    }
    learn = Learn(lock=lock,
                  extractors=extractors,
                  preprocessed_path=preprocessedPath,
                  input_path=inputPath,
                  sampling='test',
                  combined_scorer=None, queue=a_queue)
    return learn



if __name__ == '__main__':

    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    log.addHandler(sh)

    # thread safe queue
    q = queue.Queue()
    lock = threading.Lock()  # Wordnet is not threadsave

    # WHO, WHAT
    #weights = load_best_weights('./result/training_final_result_what_1.json')
    #q.put(action(lock, weights))


    # WHERE
    weights = load_best_weights('./result/training_final_result_where_1.json')
    q.put(environment_where(lock, weights))

    # WHEN
    #weights = load_best_weights('./result/training_final_result_when_1.json')
    #q.put(environment_when(lock, weights))

    # WHY
    #weights = load_best_weights('./result/training_final_result_why_1.json')
    #q.put(cause(lock, weights))

    # HOW
    #weights = load_best_weights('./result/training_final_result_how_1.json')
    #q.put(method(lock, weights))

    for i in range(4):
            t = Worker(q)
            t.daemon = True
            t.start()

    # wait till all extractors are done
    q.join()
