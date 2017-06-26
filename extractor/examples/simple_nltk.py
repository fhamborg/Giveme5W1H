import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from extractor.extractor import FiveWExtractor
from extractor.document import DocumentFactory
from extractor.preprocessors.preprocessor_nltk import Preprocessor
from extractor.extractors import action_extractor, environment_extractor, cause_extractor

"""
ATTENTION: This example uses the depreciated nltk preprocessor. For the updated version see simple_core_nlp.py.

This is a simple example on how to use the extractor with the nltk preprocessor.
Articles are entered trough the console.

Please update the path to the Stanford NER Tagger.
"""

# Path to the Standford NER Tagger jar,
# can be found at https://nlp.stanford.edu/software/CRF-NER.shtml#Download
stanford_ner_jar = '/extractor/resources/stanford-ner/stanford-ner.jar'


if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    preprocessor = None
    try:
        if os.path.isabs(stanford_ner_jar):
            # get the absolute path
            stanford_ner_jar = os.path.dirname(os.path.dirname(__file__)) + stanford_ner_jar

        preprocessor = Preprocessor(stanford_ner_jar)

    except LookupError as e:
        log.error('%s\nThe Stanford NER can be downloaded at https://nlp.stanford.edu/software/CRF-NER.' % e)

    if preprocessor is not None:

        # If desired, the selection of extractors can changed and passed to the FiveWExtractor at initialization
        extractor_list = [
            # action_extractor.ActionExtractor(),
            # the nltk preprocessor doesn't support the action_extractor anymore!
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

