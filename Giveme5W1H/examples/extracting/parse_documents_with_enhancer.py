import logging
import os

from enhancer.aida import Aida
from enhancer.heideltime import Heideltime
from Giveme5W1H.extractors import action_extractor, cause_extractor, environment_extractor
from Giveme5W1H.extractors import method_extractor

from Giveme5W1H.extractor.extractor import MasterExtractor
from Giveme5W1H.extractor.tools.file.handler import Handler

# Add path to allow execution though console
# sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))

"""
Advanced example to use the extractor in combination with NewsPlease files
 - The output of the core_nlp_host is saved in the cache directory to speed up multiple runs. 
 - Documents are preload into memory and stay persistent for further calculations.
 - Enhancer is used to process the result further

Documents are preprocessed just once, you have to set is_preprocessed to false, 
if you want to process them again by core_nlp (or just delete cache and output)
"""
if __name__ == '__main__':
    # helper to setup a correct path
    rel_datasets_path = '/../datasets/'
    dataset_helper = {
        'gold_standard': os.path.dirname(__file__) + rel_datasets_path + 'gold_standard',
        'bbc': os.path.dirname(__file__) + rel_datasets_path + 'bbc',
        'google_news': os.path.dirname(__file__) + rel_datasets_path + 'google_news',
        'news_cluster': os.path.dirname(__file__) + rel_datasets_path + 'news_cluster',
        'local': os.path.dirname(__file__)
    }

    #
    # Switch here between the predefined datasets or local for the local folder
    #
    basePath = dataset_helper['news_cluster']
    #
    #
    #

    # logger setup
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    # giveme5w setup
    extractor = MasterExtractor(extractors=[
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor(),
        method_extractor.MethodExtractor()
    ], enhancement=[
         Heideltime(['when']),
         Aida(['how', 'when', 'why', 'where', 'what', 'who'])
    ])

    inputPath = basePath + '/data'
    outputPath = basePath + '/output'
    preprocessedPath = basePath + '/cache'

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
            # .set_limit(1)

            # Optional: resume ability, skip input file if its already in output
            .skip_documents_with_output()

            # load and saves all document runtime objects for further programming
            # .preload_and_cache_documents()

            ## setup is done: executing it
            .process()

        # get the processed documents, this can only be done because preload_and_cache_documents was called
        # .get_documents()
    )
