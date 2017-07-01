import logging
import os
import sys

from extractor.extractor import FiveWExtractor, factoryBuilder
from extractor.extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from extractor.tools.news_please.handler import Handler


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

    extractor = factoryBuilder()
    inputPath = os.path.dirname(__file__) + '/input'
    outputPath = os.path.dirname(__file__) + '/output'
    
    
    # initiate the newsplease file handler with the input directory
    ( Handler(inputPath)
        # add an optional output directory
       .setOutputPath(outputPath)
        # limit the the to process documents (nice for development) 
       .setLimit(1)
        # add an optional extractor (it would do basically just copying without...)
       .setExtractor(extractor)
        # executing it
       .process().getDocuments())
            
    