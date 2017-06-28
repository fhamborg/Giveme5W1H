import logging
import os
import sys
from pip.req.req_file import preprocess
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))

from extractor.extractor import FiveWExtractor
from extractor.tools.news_please.handler import Handler
from extractor.extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
"""
This is a simple example on how to use the extractor in combination with NewsPlease files
"""

# don`t forget to start up core_nlp_host
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    
    extractor = FiveWExtractor(extractors = [
                        #action_extractor.ActionExtractor(),
                        #environment_extractor.EnvironmentExtractor(),
                        cause_extractor.CauseExtractor(),
                        #method_extractor.MethodExtractor()
                    ])
    inputPath = os.path.dirname(__file__) + '/input'
    outputPath = os.path.dirname(__file__) + '/output'
    preprocessedPath = os.path.dirname(__file__) + '/cache'
    
    documents = (
                # initiate the newsplease file handler with the input directory
                Handler(inputPath)
                    # add an optional output directory
                   .setOutputPath(outputPath)
                    # set a path to save an load preprocessed documents
                   .setPreprocessedPath(preprocessedPath)
                    # limit the the to process documents (nice for development) 
                   .setLimit(1)
                    # add an optional extractor (it would do basically just copying without...)
                   .setExtractor(extractor)
                    # saves all document objects for further programming
                   .preLoadAndCacheDocuments()
                    # executing it
                   .process().getDocuments()
            )
    