import os
import pickle
import numpy as np
import time


class WorkQueue(object):

    def __init__(self):

        self._weights_range = None
        self.phrase_range_location = None
        self.phrase_range_time_date = None
        self.time_range = None
        self._queue = None
        self._queue_processed = None
        self._queue_path = os.path.dirname(__file__) + '/cache/queue.prickle'
        self._queue_processed_path = os.path.dirname(__file__) + '/cache/queue_processed.prickle'

    def get_queue_count(self):
        return len(self._queue)

    def setup_scoring_parameters(self,  weight_start: float = 0.05 , weight_stop: float = 1, weight_step_size: float = 0.05):
        self._weights_range = np.arange(weight_start, weight_stop, weight_step_size)

    def setup_extracting_parameters(self, phrase_range_location: np.arange = np.arange(3, 4), phrase_range_time_date: np.arange=np.arange(1, 3), time_range: np.arange=np.arange(86400, 86401)):
        self.phrase_range_location = phrase_range_location
        self.phrase_range_time_date = phrase_range_time_date
        self.time_range = time_range

    def load(self):
        if os.path.isfile(self._queue_path) and os.path.isfile(self._queue_processed_path):
            # _preprocessedPath path is given, and there is already a preprocessed document
            with open(self._queue_path, 'rb') as ff:
                self._queue = pickle.load(ff)

            with open(self._queue_processed_path, 'rb') as ff:
                self._queue_processed = pickle.load(ff)

            print("weightinstance found! continue processing :)")


        else:
            print('generating a new queues')
            self._generate()



    def resolve_document(self, last_item,  dId, result):
        """
        adds the quee item adds the result and attached if per document to
        queue_processed

        :param result:
        :return:
        """
        last_item['dId'] = dId
        last_item['result'] = result
        self._queue_processed.append(result)

        return last_item

    def pop(self, persist: bool = True):
        """
        takes an item from the process queue. and attached it with the result to the
        queue_processed queue

        :param result:
        :return:
        """
        self._queue.pop()
        if persist:
            with open(self._queue_path, 'wb') as f:
                # Pickle the 'data' document using the highest protocol available.
                pickle.dump(self._queue, f, pickle.HIGHEST_PROTOCOL)

            with open(self._queue_processed_path, 'wb') as f:
                # Pickle the 'data' document using the highest protocol available.
                pickle.dump(self._queue_processed, f, pickle.HIGHEST_PROTOCOL)




    def next(self):
        if len(self._queue) > 0:
            return self._queue[-1]
        return None

    def _generate(self):
        """

        https://www.hackmath.net/en/calculator/combinations-and-permutations?n=19&k=4&order=1&repeat=1

        :return:
        """
        self._queue_processed = []
        self._queue = []
        extracting_parameters_id = 0

        # because of the combined scoring each range must be respected separate
        for phrase_range_location in self.phrase_range_location:
            for phrase_range_time_date in self.phrase_range_time_date:
                for time_range in self.time_range:
                    #
                    # generate weights for these extracting parameters
                    #
                    extracting_parameters_id = extracting_parameters_id

                    for i in self._weights_range:
                        for j in self._weights_range:
                            for k in self._weights_range:
                                for l in self._weights_range:
                                    self._queue.append({
                                       'extracting_parameters_id': extracting_parameters_id,
                                       'scoring_parameters': {
                                           'weights': (i, j, k, l)
                                       },
                                       'extracting_parameters': {
                                           'phrase_range_location': phrase_range_location,
                                           'phrase_range_time_date': phrase_range_time_date,
                                           'time_range': time_range
                                       }})
                    extracting_parameters_id = extracting_parameters_id + 1



