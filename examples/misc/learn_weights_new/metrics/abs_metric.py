from abc import abstractmethod

from misc.learn_weights_new.entities_strategy.best import Best
from tools.cache_manager import CacheManager


class AbsMetric(object):
    def __init__(self, cache_dir='../examples/caches', pre_processors=None, multipleEntitiesStrategy=Best()):
        """
         Initiates the extractor, weights can be passed to overwrite default settings.

        :param weight:
        :param accessor: path to the list of candidates. this is passed to pre_process
        :param id: an optional name, to make metrics for the same accessor
        """

        self._id = None

        self._cache = CacheManager.instance().get_cache(cache_dir + '/metric_' + str(self.__class__.__name__))

        self._pre_processors = pre_processors
        self._multipleEntitiesStrategy = multipleEntitiesStrategy

    def get_cache(self):
        return self._cache

    def get_normalisation(self):
        return self._normalisation

    def get_id(self):
        return self._id

    def get_weight(self):
        return self._weight

    def get_pre_processors(self):
        return self._pre_processors

    def get_accessor(self):
        return self._accessor

    def get_distance(self, candidates_a, candidates_b):
        """
        candidates_a & candidates_b is the return val pre_process per document
        :param candidates_a:
        :param candidates_b:
        :return:
        """

        if isinstance(candidates_a, list) and isinstance(candidates_b, list):
            # support for multiple entities
            if len(candidates_a) > 0 and len(candidates_b) > 0:
                # two lists with at least one entry
                result = self._multipleEntitiesStrategy.process(self, candidates_a, candidates_b)
            else:
                # not comparable
                return None
        elif candidates_a and candidates_b and candidates_a != 'NULL' and candidates_b != 'NULL':
            # support for simple enmities
            result = self.calculate_distance(candidates_a, candidates_b)
        else:
            return None

        return result

    @abstractmethod
    def calculate_distance(self, candidates_a, candidates_b):
        """
        candidates_a & candidates_b is the return val pre_process per document
        :param candidates_a:
        :param candidates_b:
        :return:
        """
        return None
