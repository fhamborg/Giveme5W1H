import logging
import queue
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


def method():
    a_queue = WorkQueue(generator='method')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'method': method_extractor.MethodExtractor()
    }

    learn = Learn(extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def cause():
    a_queue = WorkQueue(generator='cause')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'cause': cause_extractor.CauseExtractor()
    }

    learn = Learn(extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def environment():
    a_queue = WorkQueue(generator='environment')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'environment': environment_extractor.EnvironmentExtractor(),
        # 'cause': cause_extractor.CauseExtractor(),
        # 'method': method_extractor.MethodExtractor()
    }

    learn = Learn(extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


def action():
    a_queue = WorkQueue(generator='action')
    a_queue.setup_scoring_parameters()
    a_queue.setup_extracting_parameters()
    a_queue.load()

    extractors = {
        'action': action_extractor.ActionExtractor(),
        # 'environment': environment_extractor.EnvironmentExtractor(),
        # 'cause': cause_extractor.CauseExtractor(),
        # 'method': method_extractor.MethodExtractor()
    }
    learn = Learn(extractors=extractors, preprocessed_path=preprocessedPath, input_path=inputPath,
                  combined_scorer=None, queue=a_queue)
    return learn


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')

    # sh = logging.StreamHandler()
    # sh.setLevel(logging.INFO)
    # log.addHandler(sh)

    # thread safe queue
    q = queue.Queue()

    # basic leaner
    log.setLevel(logging.WARNING)
    # q.put(action())
    # q.put(environment())
    # q.put(cause())
    q.put(method())
    log.setLevel(logging.INFO)
    # creating worker threads
    for i in range(4):
        t = Worker(q)
        t.daemon = True
        t.start()

    # wait till oll extractors are done
    q.join()
