from abc import abstractmethod


class AbsEntitiesStrategy(object):
    def __init__(self):
        self._values = []

    def process(self, metric, candidates_a: list, candidates_b: list):
        """
        handles metrics, when each candidate has multiple entities.
        For example
         - one "what" has two different wikidata nodes within one answer
         - or simply if a document is compared using the first 5 candidates

         default implementation compares all with all. and calls track for each result

        :param metric:
        :param candidates_a:
        :param candidates_b:
        :return:
        """
        for candidate_a in candidates_a:
            for candidate_b in candidates_b:
                if candidate_a is not None and candidate_b is not None:
                    result = metric.calculate_distance(candidate_a, candidate_b)
                    self._track(result)

    def _track(self, value):
        self._values.append(value)

    def get_result(self):
        result = self._callcualte_result()
        self._values = []
        return result

    @abstractmethod
    def _calculate_result(self):
        pass
