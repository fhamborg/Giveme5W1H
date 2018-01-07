import logging

from misc.learn_weights.entities_strategy.abs_entities_strategy import AbsEntitiesStrategy


class Average(AbsEntitiesStrategy):
    """
    returns the best value (under the light of metrics and distances this menas the smalles value it taken)
    calculate
    """

    def _calculate_result(self):
        if len(self._values) > 0:
            return sum(self._values) / len(self._values)
        else:
            logging.error('AbsEntitiesStrategy:Average: there was no result. This should not happen')
