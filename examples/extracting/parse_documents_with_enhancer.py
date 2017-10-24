import logging
import os


from Giveme5W_enhancer.heideltime import Heideltime

from extractor.configuration import Configuration as Config
from extractor.extractor import FiveWExtractor
from extractor.tools.file.handler import Handler
from extractors import environment_extractor
from extractors import method_extractor
from extractors import action_extractor
from extractors import cause_extractor

# Add path to allow execution though console
#sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))

"""
Advanced example to use the extractor in combination with NewsPlease files
 - The output of the core_nlp_host is saved in the cache directory to speed up multiple runs. 
 - Documents are preload into memory and stay persistent for further calculations.
 - Enhancer is used to process the result further

Documents are preprocessed just once, you have to set is_preprocessed to false, 
if you want to process them again by core_nlp (or just delete cache and output)
"""
if __name__ == '__main__':

    # helper to make dataset selction simple
    dataset_golden_standard = os.path.dirname(__file__) + '/../datasets/gold_standard/data/'
    # Do not work with heideltime!, there is no pub date...
    dataset_bbc = os.path.dirname(__file__) + '/../datasets/bbc/data/'

    # logger setup
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    # giveme5w setup
    extractor = FiveWExtractor(extractors=[
        #action_extractor.ActionExtractor(),
        #environment_extractor.EnvironmentExtractor(),
        #cause_extractor.CauseExtractor(),
        method_extractor.MethodExtractor()
    ], enhancement=[
        Heideltime(['when']),
        #Aida(['how','when','why','where','what','who'])
    ])

    inputPath = dataset_golden_standard
    outputPath = os.path.dirname(__file__) + '/output'

    preprocessedPath = os.path.dirname(__file__) + '/cache'

    documents = (
        # initiate the file handler with the input directory
        Handler(inputPath)
            # add giveme5w extractor  (it would only copying files without...)
            .set_extractor(extractor)

            # Optional: set a output directory
            .set_output_path(outputPath)

            # Optional: set a path to cache and load preprocessed documents (CoreNLP & Enhancer result)
            .set_preprocessed_path(preprocessedPath)

            # Optional: limit the documents read from the input directory (handy for development)
            .set_limit(1)

            # Optional: resume ability, skip input file if its already in output
            #.skip_documents_with_output()

            # load and saves all document runtime objects for further programming
            .preload_and_cache_documents()

            ## setup is done: executing it
            .process()

            # get the processed documents, this can only be done because preload_and_cache_documents was called
            .get_documents()
    )
