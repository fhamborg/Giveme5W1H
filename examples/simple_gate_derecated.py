import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
from timeit import default_timer as timer
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractor import FiveWExtractor
from extractor.tools import gate_reader
from extractor.tools.csv_writer import CSVWriter

"""
This is a simple example on how to use the extractor in combination with our GATE reader.
This script extracts the five W answers from the text and creates csv to compare the results with the GATE annotations.

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

    # init extractor
    preprocessor = Preprocessor(core_nlp_host)
    extractor = FiveWExtractor(preprocessor)

    # open files with the gate reader
    documents = gate_reader.parse_dir(os.path.dirname(__file__) + '/sample_articles')
    start_all = timer()

    with CSVWriter(os.path.expanduser('~') + '/giveme5w.csv') as writer:
        log.info("Starting parsing of %i documents " % len(documents))
        for document in documents:
            start = timer()
            extractor.parse(document)
            log.info("Document parsed in %is" % (timer() - start))

            answers = document.get_answers()

            # write results into csv file, the second parameter determines the number of candidates to save
            writer.save_document(document, 3)

    diff_all = timer() - start_all
    log.info("total time={}, time/article={}".format(round(diff_all, 2), round(diff_all / len(documents), 2)))
