'''
helper script to demonstrate the entire learn weights process pipeline.

CLEAR /queue_caches/ and result folder before running !!!!!!!!!!
Evaluate can`t distinguish between old and new results.

'''
import logging
import queue
import threading

from misc.learn_weights import run_training, run_test
from misc.learn_weights.evaluate import process_files
from misc.learn_weights.learn import Worker
from misc.learn_weights.run_test import load_best_weights


def create_worker(q):
    for i in range(4):
        t = Worker(q)
        t.daemon = True
        t.start()


def get_queue_wth_lock_and_worker():
    # queue for multi threading support
    q = queue.Queue()
    # Wordnet is not threadsave...
    lock = threading.Lock()
    # Working threads
    create_worker(q)

    return q, lock


def load_trainer_for_question(q, questions):
    for question in questions:
        if question == 'who' or question == 'what':
            q.put(run_training.action(lock))
        elif question == 'why':
            q.put(run_training.cause(lock))
        elif question == 'where':
            q.put(run_training.environment_where(lock))
        elif question == 'when':
            q.put(run_training.environment_when(lock))
        elif question == 'how':
            q.put(run_training.method(lock))
        elif question == 'cs':
            q.put(run_training.default_combined_scoring(lock))


def load_tester_for_question(q, questions):
    for question in questions:
        weights = load_best_weights('./result/training_final_result_' + question + '_1.json')
        if question == 'who' or question == 'what':
            q.put(run_test.action(lock, weights))
        elif question == 'why':
            q.put(run_test.cause(lock, weights))
        elif question == 'where':
            q.put(run_test.environment_where(lock, weights))
        elif question == 'when':
            q.put(run_test.environment_when(lock, weights))
        elif question == 'how':
            q.put(run_test.method(lock, weights))
        elif question == 'cs':
            q.put(run_test.default_combined_scoring(lock, weights))


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    log.addHandler(sh)

    # who and what are using them same trainer. Declare just one !!!

    # its recommended to run one by one to keep memory print low
    # questions = ['who','why', 'where', 'when', 'how']
    #learn_questions = ['what']  # output is also  who
    #learn_questions = ['why']
    # learn_questions = ['where']
    # learn_questions = ['when']
     #learn_questions = ['how']
    learn_questions = ['how','what','why']


    #
    # Training - to find the best weights
    #
    q, lock = get_queue_wth_lock_and_worker()

    load_trainer_for_question(q, learn_questions)

    # wait till all trainings are done
    q.join()

    #
    # Training - evaluate
    #

    # evaluate results - by cecking all subfolders for processd woking parts
    process_files('queue_caches/*_processed*/', praefix='training')





    #
    # Test - with the best weights - found with training/evaluation
    #
    q, lock = get_queue_wth_lock_and_worker()

    load_tester_for_question(q, learn_questions)

    #
    # Test - evaluate
    #
    process_files('queue_caches/*pre_calculated_processed*/', praefix='test')

    print('done')
