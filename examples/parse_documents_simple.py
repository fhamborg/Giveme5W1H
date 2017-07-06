import logging
import os
import sys

from extractor.extractor import FiveWExtractor
from extractor.tools.file.handler import Handler

# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))

"""
This is a simple example how to use the extractor in combination with NewsPlease files.
File will be process one by one, nothing is cached
"""

# don`t forget to start up core_nlp_host
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    extractor = FiveWExtractor()
    inputPath = os.path.dirname(__file__) + '/input'
    outputPath = os.path.dirname(__file__) + '/output'

    # initiate the news-please file handler with the input directory
    (Handler(inputPath)
    # everything else is optional:

        ## add an optional output directory
             .set_output_path(outputPath)
             # limit the documents read from the input directory (handy for development)
             .set_limit(1)
             # add an extractor
             .set_extractor(extractor)

         ## setup is done:
             # executing it
             .process())
