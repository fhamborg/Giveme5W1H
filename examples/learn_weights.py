import logging
import os
import sys
# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
#from timeit import default_timer as timer
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.extractor import FiveWExtractor

from extractor.tools.news_please.handler import Handler


core_nlp_host = 'http://localhost:9000'

def adjustWeights(extractors, i,j,k,l):
    # 1_Change weights 
    ## (action_0, cause_1, environment_2)
    extractors[0].weights = (i, j, k)
    ## time
    extractors[1].weights = ((i, j), (i, j, k, l))
    ## cause - (position, conjunction, adverb, verb)
    extractors[2].weights = (i, j, k, l)




if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    
    # Setup
    extractor = FiveWExtractor(Preprocessor(core_nlp_host))
    inputPath = os.path.dirname(__file__) + '/input/'
    
    increment_range = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                   0.85, 0.90, 0.95, 1]
    
    # Put all together, run it once, get the cached document objects
    documents = Handler(inputPath).setExtractor( extractor ).preLoadAndCacheDocuments().process().getDocuments()
    
    for document in documents:
        # manually generate candidate lists
        # candidates = [e._extract_candidates(document) for e in extractor.extractors]
        
        # try all weight combinations
        for i in increment_range:
            for j in increment_range:
                for k in increment_range:
                    for l in increment_range:
                        
                        adjustWeights(extractor.extractors)
                    
                        # 2__Reevaluate per extractor
                        for extractor in extractor.extractors:
                            extractor._evaluate_candidates(document)
                                        
                        # 2_1 Reevaluate combined scoring
                        for combinedScorer in extractor.combinedScorers:
                            combinedScorer.score(document)
                    
                        # 3__ calculate the distance to annotation 
                        # 3_1 Time
                        extractor.extractors[1]._distCandidateToAnnotation(document)
                        # 3_2 Cause extractor - (position, conjunction, adverb, verb)
                        extractor.extractors[2]._distCandidateToAnnotation(document)
                        
                    # 3_3 action extractor - (position, frequency, named entity)
                    extractor.extractors[0]._evaluate_candidates(document, candidates[0])
                    extractor.extractors[0]._distCandidateToAnnotation(document)