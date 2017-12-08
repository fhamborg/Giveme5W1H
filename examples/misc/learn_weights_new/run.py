import logging
import queue
import threading
from threading import Thread

from extractor.root import path
from extractors import environment_extractor, action_extractor, cause_extractor, method_extractor
from misc.learn_weights_new.learn import Learn
from misc.learn_weights_new.work_queue import WorkQueue

inputPath = path('../examples/datasets/gold_standard/data')
preprocessedPath = path('../examples/datasets/gold_standard/cache')


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


def method(lock):
    a_queue = WorkQueue(generator='method')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'method': method_extractor.MethodExtractor()
    }

    learn = Learn(lock=lock,extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def cause(lock):
    a_queue = WorkQueue(generator='cause')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'cause': cause_extractor.CauseExtractor()
    }

    learn = Learn(lock=lock,extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def environment(lock):
    a_queue = WorkQueue(generator='environment')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'environment': environment_extractor.EnvironmentExtractor()
    }

    learn = Learn(lock=lock,extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def action(lock):
    a_queue = WorkQueue(generator='action')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'action': action_extractor.ActionExtractor()
        # 'environment': environment_extractor.EnvironmentExtractor(),
        # 'cause': cause_extractor.CauseExtractor(),
        # 'method': method_extractor.MethodExtractor()
    }
    learn = Learn(lock=lock,extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
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
    lock = threading.Lock() # Wordnet is not threadsave

    # basic learner
    log.setLevel(logging.ERROR)
    q.put(action(lock))
    q.put(environment(lock))
    q.put(cause(lock))
    q.put(method(lock))
    log.setLevel(logging.INFO)
    # creating worker threads
    for i in range(4):
        t = Worker(q)
        t.daemon = True
        t.start()

    # wait till all extractors are done
    q.join()
