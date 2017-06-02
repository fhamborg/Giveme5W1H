import logging
import os
import sys
import glob
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
#from timeit import default_timer as timer
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractor import FiveWExtractor

from extractor.tools.news_please.writer import Writer
from extractor.tools.news_please.reader import Reader


"""
This is a simple example on how to use the extractor in combination with NewsPlease files
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
    #preprocessor = Preprocessor(core_nlp_host)
    #extractor = FiveWExtractor(preprocessor)
    
    writer = Writer(os.path.dirname(__file__) + '/result')
    reader = Reader()
    
    # open files with the gate reader
    for filepath in glob.glob(os.path.dirname(__file__) + '/sample_articles/*.json'):
        document = reader.read(filepath)
        # TODO extracting
        # extractor.parse(document)
        writer.write(document)
    
    #start_all = timer()  
    #diff_all = timer() - start_all
    #log.info("total time={}, time/article={}".format(round(diff_all, 2), round(diff_all / len(documents), 2)))