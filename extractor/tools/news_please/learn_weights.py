import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
#from timeit import default_timer as timer
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractor import FiveWExtractor


from extractor.tools.news_please.handler import Handler
from extractor.tools.news_please.processor.learn_weights import LearnWeights

"""

"""

core_nlp_host = 'http://localhost:9000'

if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    
    #extractor = FiveWExtractor(Preprocessor(core_nlp_host))
    inputPath = os.path.dirname(__file__) + '/input/'
    outputPath = os.path.dirname(__file__) + '/output'
    LearnWeightsProcessor = LearnWeights()
    handler = Handler(inputPath).setOutputPath(outputPath).addProcessor( LearnWeights() )
    
    increment_range = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                   0.85, 0.90, 0.95, 1]
    
    for i in increment_range:
        for j in increment_range:
            for k in increment_range:
                for l in increment_range:
                    # TODO change weights
                    
                    # process again
                    handler.process()
    # get results from LearnWeightsProcessor
    #