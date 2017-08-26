import logging

#
# Random metric, it will always return a distance between 0 and 1
from Giveme5W_enhancer.enhancers.heideltime import Heideltime


class Enhancement():

    def __init__(self, config=None):
        self.log = logging.getLogger('GiveMe5W-Enhancer')
        self.log.info('Enhancer initialised')
        self._config = config

        self._enhancers = [
            Heideltime()
        ]

    def process(self, document):
        self.log.info('            ')
        self.log.info('      Enhancer process:')

        for enhancer in self._enhancers:
            enhancer.enhance(document)

        self.log.info('      Enhancer finished')