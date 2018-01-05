import logging
import os
import pathlib
import pickle

import numpy as np
import copy

from extractors.method_extractor import ExtensionStrategy


class WorkQueue(object):
    def __init__(self, id: str = None, generator: str = 'default', pre_calculated_weights=None):
        """

        :param id:
        :param generator: method to generate a _queue
        """
        if id:
            self._id = id + '_' + generator
        else:
            self._id = generator
        self._weights_range = None
        self.phrase_range_location = None
        self.phrase_range_time_date = None
        self.time_range = None
        self._pre_calculated_weights = pre_calculated_weights
        self._queue = []
        self._queue_path_dir =  os.path.dirname(__file__) + '/queue_caches/'
        self._queue_path = self._queue_path_dir + self._id + '_queue.pickle'
        self._processed_items_path = self._queue_path_dir + '/' + self._id + '_processed_items/'
        pathlib.Path(self._processed_items_path).mkdir(parents=True, exist_ok=True)

        self._unique_weights = {}
        self._log = logging.getLogger('GiveMe5W')

        if generator is None:
            self._generator = self._generate_full_combination
        else:
            self._generator = generator

    def get_queue_count(self):
        return len(self._queue)

    def get_id(self):
        return self._id

    def setup_scoring_parameters(self, weight_start: float = 0.0, weight_stop: float = 1.1,
                                 weight_step_size: float = 0.1):
        self._weights_range = np.arange(weight_start, weight_stop, weight_step_size)

    def setup_extracting_parameters(self, phrase_range_location: np.arange = np.arange(3, 4),
                                    phrase_range_time_date: np.arange = np.arange(1, 2),
                                    time_range: np.arange = np.arange(86400, 86401)):
        self.phrase_range_location = phrase_range_location
        self.phrase_range_time_date = phrase_range_time_date
        self.time_range = time_range

    def load(self):
        if os.path.isfile(self._queue_path):
            with open(self._queue_path, 'rb') as ff:
                self._queue = pickle.load(ff)
            self._log.info("queue found! continue processing :)")
        else:
            self._log.info('generating a new queue')

            if self._generator == 'default':
                self._generate_default()
            elif self._generator == 'method':
                self._generate_method()
            elif self._generator == 'cause':
                self._generate_cause()
            elif self._generator == 'environment':
                self._generate_environment()
            elif self._generator == 'environment_where':
                self._generate_environment_where()
            elif self._generator == 'environment_when':
                self._generate_environment_when()
            elif self._generator == 'action':
                self._generate_action()
            elif self._generator == 'combined_scoring':
                self._generate_combined_scoring()
            elif self._generator == 'pre_calculated':
                self._generate_pre_calculated(self._pre_calculated_weights)


    def resolve_document(self, last_item, dId, result, document_index):
        """
        takes a queue item, attached result per document, and appends it to queue_processed

        :param result:
        :return:
        """
        unique_index = str(len(self._queue)) + '_' + str(document_index)
        last_item['dId'] = dId
        last_item['result'] = result

        self.persist_processed_item(unique_index, last_item)

    def pop(self, persist: bool = True):
        self._queue.pop()
        if persist:
            self.persist()

    def persist_processed_item(self, id, item):
        with open(self._processed_items_path + id + '.pickle', 'wb') as f:
            pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

    def persist(self):
        with open(self._queue_path, 'wb') as f:
            # Pickle the 'data' document using the highest protocol available.
            pickle.dump(self._queue, f, pickle.HIGHEST_PROTOCOL)

    def next(self):
        if len(self._queue) > 0:
            return self._queue[-1]
        return None

    def vector_is_unique(self, weights):
        """
        this is refusing vectors with the same weight ratio, if one was already used
        e.g
        [0.1, 0,1] and [0.2, 0,2]
        [0.2, 0,4] and [0.4, 0,8]


        - sets the first not null weight to * 1000 (int) (overcome floating error)
        - scales all other weights with the same factor
        - stores string rep. to be combarable with other vectors

        :param weights:
        :return:
        """
        if sum(weights) == 0:
            return False

        # set se first not null weight to * 1000 (int) (overcome floating error)
        for weight in weights:
            if weight != 0:
                scaleFactor = 10000 / weight
                break
        # scale vector
        scaled_weights = []
        for weight in weights:
            # if weight != 0:
            scaled_weights.append(int(scaleFactor * weight))

        # build a string representation
        scaled_weights_string = [str(x) for x in scaled_weights]
        scaled_weights_string = ''.join(scaled_weights_string)

        if self._unique_weights.get(scaled_weights_string, False):
            return False
        else:
            self._unique_weights[scaled_weights_string] = True
            return True

    def _generate_pre_calculated(self, pre_calculated_weights):
        for pre_calculated_weight in pre_calculated_weights:
            self._queue.append({
                'extracting_parameters_id': 1,
                'scoring_parameters': {
                    'weights': pre_calculated_weight
                },
                'extracting_parameters': {
                    'extension_strategy': None
                }})

    def _generate_method(self):
        # (float, float)
        #for pm, extracting_parameters in enumerate([ExtensionStrategy.Range, ExtensionStrategy.Blacklist]):
        for i in self._weights_range:
            for j in self._weights_range:
                for k in self._weights_range:
                    for l in self._weights_range:
                        weights = (i, j, k, l)
                        if self.vector_is_unique(weights):
                            self._queue.append({
                                'extracting_parameters_id': 1,
                                'scoring_parameters': {
                                    'weights': weights
                                },
                                'extracting_parameters': {
                                    'extension_strategy': {}
                                }})

    def _generate_cause(self):
        # (float, float, float, float)
        for i in self._weights_range:
            for j in self._weights_range:
                for k in self._weights_range:
                    for l in self._weights_range:
                        weights = (i, j, k, l)
                        if self.vector_is_unique(weights):
                            self._queue.append({
                                'extracting_parameters_id': 1,
                                'scoring_parameters': {
                                    'weights': weights
                                },
                                'extracting_parameters': {}})

    def _generate_environment_when(self):
        weight_start = 0
        weight_step_size = 0.1
        weight_stop = 1
        # (0.5, 0.8), (0.8, 0.7, 0.5, 0.5, 0.5)
        for i in self._weights_range:
            for j in self._weights_range:
                for k in self._weights_range:
                    for l in self._weights_range:
                        for m in self._weights_range:
                            weights = (i, j, k, l, m)
                            if self.vector_is_unique(weights):
                                self._queue.append({
                                    'extracting_parameters_id': 1,
                                    'scoring_parameters': {
                                        'weights': weights
                                    },
                                    'extracting_parameters': {}})
    def _generate_environment_where(self):
        weight_start = 0
        weight_step_size = 0.1
        weight_stop = 1
        # (0.5, 0.8), (0.8, 0.7, 0.5, 0.5, 0.5)
        for i in self._weights_range:
            for j in self._weights_range:
                weights = (i, j)
                if self.vector_is_unique(weights):
                    self._queue.append({
                        'extracting_parameters_id': 1,
                        'scoring_parameters': {
                            'weights': weights
                        },
                        'extracting_parameters': {}})

    def _generate_environment(self):
        weight_start = 0
        weight_step_size = 0.1
        weight_stop = 1
        # (0.5, 0.8), (0.8, 0.7, 0.5, 0.5, 0.5)
        for i in self._weights_range:
            for j in self._weights_range:
                for k in np.arange(weight_start, weight_stop, weight_step_size):
                    for l in np.arange(weight_start, weight_stop, weight_step_size):
                        for m in np.arange(weight_start, weight_stop, weight_step_size):
                            for n in np.arange(weight_start, weight_stop, weight_step_size):
                                for o in np.arange(weight_start, weight_stop, weight_step_size):
                                    weights = (i, j, k, l, m, n, o)
                                    if self.vector_is_unique(weights):
                                        self._queue.append({
                                            'extracting_parameters_id': 1,
                                            'scoring_parameters': {
                                                'weights': weights
                                            },
                                            'extracting_parameters': {}})

    def _generate_action(self):
        for i in self._weights_range:
            for j in self._weights_range:
                for k in self._weights_range:
                    weights = (i, j, k)
                    if self.vector_is_unique(weights):
                        self._queue.append({
                            'extracting_parameters_id': 1,
                            'scoring_parameters': {
                                'weights': weights
                            },
                            'extracting_parameters': {}})

    def _generate_combined_scoring(self):
        for i in self._weights_range:
                weights = (i, )
                if i:
                    self._queue.append({
                        'extracting_parameters_id': 1,
                        'scoring_parameters': {
                            'weights': weights
                        },
                        'extracting_parameters': {}})

    def _generate_default(self):
        """
        https://www.hackmath.net/en/calculator/combinations-and-permutations?n=19&k=4&order=1&repeat=1130321 per
        :return:
        """
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
