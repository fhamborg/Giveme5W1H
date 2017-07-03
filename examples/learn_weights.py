import logging
import os
import sys
import json

from extractor.extractor import FiveWExtractor
from extractor.tools.news_please.handler import Handler
from extractor.tools.util import cmp_date, cmp_text

# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
#from timeit import default_timer as timer


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
    extractorObject = FiveWExtractor()
    inputPath = os.path.dirname(__file__) + '/input/'
    preprocessedPath = os.path.dirname(__file__) + '/cache'

    increment_range = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                   0.85, 0.90, 0.95, 1]
    
    # Put all together, run it once, get the cached document objects
    documents = (
        # initiate the newsplease file handler with the input directory
        Handler(inputPath)
            # set a path to save an load preprocessed documents
            .setPreprocessedPath(preprocessedPath)
            # limit the the to process documents (nice for development)
            .setLimit(1)
            # add an optional extractor (it would do basically just copying without...)
            .setExtractor(extractorObject)
            # saves all document objects for further programming
            .preLoadAndCacheDocuments()
            # executing it
            .process().getDocuments()
    )

    resultPath = os.path.dirname(__file__)+'/result/learnWeights.json'

    with open(resultPath, encoding='utf-8', mode='r') as data_file:
        data = json.load(data_file)

        # grab utilities to parse dates and locations from the EnvironmentExtractor
        geocoder = extractorObject.extractors[1].geocoder
        calendar = extractorObject.extractors[1].calendar

        # Questions

        for document in documents:
            # manually generate candidate lists
            # candidates = [e._extract_candidates(document) for e in extractor.extractors]

            # try all weight combinations
            for i in increment_range:
                for j in increment_range:
                    for k in increment_range:
                        for l in increment_range:

                            adjustWeights(extractorObject.extractors, i, j, k, l)

                            # 2__Reevaluate per extractor
                            for extractor in extractorObject.extractors:
                                extractor._evaluate_candidates(document)

                            # 2_1 Reevaluate combined scoring
                            for combinedScorer in extractorObject.combinedScorers:
                                combinedScorer.score(document)

                            annotation = document.get_annotations()
                            answers = document.get_answers()

                            # take the best annotation and compare it with the best answer
                            #when = cmp_date(annotation['when'][0][2], answers['when'][0][0][0], calendar)
                            why  = cmp_text(annotation['why'][0], answers['why'][0])
                            who  = cmp_text(annotation['who'][0], answers['who'][0])
                            what = cmp_text(annotation['what'][0], answers['what'][0])
                            how  = cmp_text(annotation['how'][0], answers['how'][0])

                            result = {
                                'when': {
                                    'weights':[i, j, k, l],
                                    'score': when
                                },
                                'why': {
                                    'weights':{
                                         'position': i,
                                         'conjunction': j,
                                         'adverb': k,
                                         'verb': l
                                    },
                                    'score': why
                                },
                                'who': {
                                    'weights':{
                                         'position': i,
                                         'frequency': j,
                                         'namedEntity': k
                                    },
                                    'score': who
                                },
                                'what': {
                                    'weights':{
                                         'position': i,
                                         'frequency': j,
                                         'namedEntity': k
                                    },
                                    'score': what
                                },
                                'how': {
                                    'weights':{
                                         'position': i,
                                         'frequency': j
                                    },
                                    'score': how
                                }
                            }

                            # save the result into result object
                            data[str(i) + str(j) + str(k) + str(l)] = result

    # save everything
    data_file.write(json.dumps(data, sort_keys=False, indent=2))

