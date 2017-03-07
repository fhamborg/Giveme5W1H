import logging

from extractor.document import DocumentFactory
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.five_w_extractor import FiveWExtractor


def _print_1w(_doc, question):
    one_w = _doc.questions[question]
    if len(one_w) == 0:
        print(question + ": NONE")
        return
    print(question + ": " + str(one_w[0]))
    if len(one_w) == 2:
        print(question + ": "+ str(one_w[1]))
        # _print_list(one_w[0][0])


def _print_5w(_doc):
    _print_1w(_doc, "who")
    _print_1w(_doc, "what")
    _print_1w(_doc, "when")
    _print_1w(_doc, "where")
    _print_1w(_doc, "why")
    print("")
    print("")


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
    factory = DocumentFactory()
    doc = extractor.parse(factory.spawn_doc(title, lead, text))
    _print_5w(doc)
