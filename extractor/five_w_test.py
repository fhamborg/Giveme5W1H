import logging
from extractor.five_w_extractor import FiveWExtractor
from extractor.tools import gate_reader
from extractor.tools.csv_writer import CSVWriter
from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.preprocessor import Preprocessor

# This is just a simple example how to use the extractor
if __name__ == '__main__':
    log = logging.Logger('FiveWTest')
    log.setLevel(20)

    # preprocessor expects the location of the sanford-ner.jar and a model to train the ner-parser
    # stanford-ner can be found here: http://nlp.stanford.edu/software/CRF-NER.shtml

    # initialize desired extractors
    extractor_list = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]

    extractor = FiveWExtractor(extractor_list)
    documents = gate_reader.parse_dir('../data/articles')

    n = 200

    with CSVWriter('../data/results.csv') as writer:
        for document in documents:
            if len(document.annotations) > 0:
                print('Parsing %s' % document.raw_title)
                extractor.parse(document)
                writer.save_document(document, 10)

                n -= 1
                if n == 0:
                    break
