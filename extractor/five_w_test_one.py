import logging

from extractor.document import Document
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.five_w_extractor import FiveWExtractor

# This is a simple example how to use the extractor. You need to fill in your data correspondingly
if __name__ == '__main__':
    log = logging.Logger('FiveWTest')
    log.setLevel(20)

    title = "add title"
    lead = "add lead paragraph"
    text = '''add text'''

    assert title != 'add title', "Change title, lead paragraph, and text first"

    # preprocessor expects the location of the sanford-ner.jar and a model to train the ner-parser
    # stanford-ner can be found here: http://nlp.stanford.edu/software/CRF-NER.shtml

    # initialize desired extractors
    extractor_list = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]

    extractor = FiveWExtractor(extractor_list)
    extractor.parse(Document(title, lead, text))
