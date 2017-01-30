import os
from extractor.preprocessor import Preprocessor
from extractor.extractors import action_extractor, environment_extractor, cause_extractor


class FiveWExtractor:

    preprocessor = None
    extractors = []

    def __init__(self, extractors=None, ner_tagger=None, ner_model=None):
        """
        :param extractors: List of Extractors
        :param ner_tagger: path to StanfordNERTagger
        :param ner_model: path to NERTagger model
        """

        if ner_tagger is None or ner_model is None:
            abs_path = os.path.dirname(__file__)
            print(abs_path)
            self.preprocessor = Preprocessor(
                abs_path + '/resources/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
                abs_path + '/resources/stanford-ner-2015-12-09/stanford-ner.jar')
        else:
            self.preprocessor = Preprocessor(ner_tagger, ner_model)

        if extractors is not None and len(extractors) > 0:
            self.extractors = extractors
        else:
            self.extractors = [
                action_extractor.ActionExtractor(),
                environment_extractor.EnvironmentExtractor(),
                cause_extractor.CauseExtractor()
            ]

    def parse(self, doc):
        """
        Extract the 5Ws for the given document

        :param doc: Document object to process
        :return: Processed document
        """
        self.preprocessor.preprocess(doc)

        for extractor in self.extractors:
            extractor.extract(doc)

        return doc
