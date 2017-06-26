import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from extractor.extractor import FiveWExtractor
from extractor.document import DocumentFactory
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractors import action_extractor, environment_extractor, cause_extractor

"""
This is a simple example on how to use the extractor with the core-nlp preprocessor.
Articles are entered trough the console.

Please update the CoreNLP address to math your host.
"""

# Host of the CoreNLP server
# For information on how to build/run a CoreNLP instance go to: https://stanfordnlp.github.io/CoreNLP/
core_nlp_host = 'http://localhost:9000'


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    preprocessor = Preprocessor(core_nlp_host)

    # If desired, the selection of extractors can changed and passed to the FiveWExtractor at initialization
    extractor_list = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]
    extractor = FiveWExtractor(preprocessor, extractor_list)

    factory = DocumentFactory()

    while True:
        title = input('Title:')
        if len(title.strip()) == 0:
            log.warning('A Document has to have a title!')
            continue
        lead = input('Lead:')
        text = input('Text:')

        doc = factory.spawn_doc(title, lead, text)
        doc = extractor.parse(doc)

        print('\n\n' + doc.pretty_answers() + '\n\n')

