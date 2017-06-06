import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
#from timeit import default_timer as timer
import extractor.extractor
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractor import FiveWExtractor

from extractor.tools.news_please.processor.simple_logger import SimpleLogger
from extractor.tools.news_please.handler import Handler
from extractor.tools.news_please.processor.learn_weights import LearnWeights
from extractor.extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
"""
This is a simple example on how to use the extractor in combination with NewsPlease files
"""

# don`t forget to start up core_nlp_host
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

core_nlp_host = 'http://localhost:9000'

if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    
    extractors = [
                #action_extractor.ActionExtractor(),
                #environment_extractor.EnvironmentExtractor(),
                #cause_extractor.CauseExtractor(),
                method_extractor.MethodExtractor()
            ]
    extractor = FiveWExtractor(Preprocessor(core_nlp_host), extractors)
    inputPath = os.path.dirname(__file__) + '/input'
    outputPath = os.path.dirname(__file__) + '/output'
    
    handler = (
                # initiate the newsplease file handler with the input directory
                Handler(inputPath)
                    # add an optional output directory
                   .setOutputPath(outputPath)
                    # limit the the to process documents (nice for development) 
                   .setLimit(1)
                    # add an optional extractor (it would do basically just copying without...)
                   .setExtractor(extractor)
                    # add an optional processor, each processor is called for each document after parsing 
                   .addProcessor( SimpleLogger() )
                   # executing the chain: reading -> extraction -> (processors) -> (writing)
                   .process()
            )
    
    