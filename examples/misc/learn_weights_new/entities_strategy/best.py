import logging

from misc.learn_weights_new.entities_strategy.abs_entities_strategy import AbsEntitiesStrategy


class Best(AbsEntitiesStrategy):
    """
    returns the best value (under the light of metrics and distances this menas the smalles value is taken)
    calculate
    """

    def _calculate_result(self):
        result = min(self._values)
        if result is not None:
            return result
        else:
            logging.error('AbsEntitiesStrategy:Best: there was no result. This should not happen')
