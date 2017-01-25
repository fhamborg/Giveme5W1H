import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import *
from bllipparser import RerankingParser


class Preprocessor:
    nerParser = None
    rerankingParser = None

    def __init__(self, classifier, ner):
        """
        Performs all necessary preprocessing

        :param classifier: Path to the Stanford NER Tagger
        :param ner: Path to the model for the NER Tagger
        """


        # init nltk tokenizers
        try:
            nltk.data.find('punkt.zip')
        except:
            nltk.download('punkt')

        # init NER parser
        self.nerParser = StanfordNERTagger(classifier, ner)

        # init Charniak parser
        self.rerankingParser = RerankingParser.fetch_and_load('WSJ+Gigaword-v2')

    def preprocess(self, document):
        """
        Performs all necessary preprocessing

        :param document: Document object to preprocess.
        :return Document: The processed Document object.
        """

        length = 0
        for section in [document.raw_title, document.raw_description, document.raw_text]:
            document.section_offsets.append(document.length)
            if section is not None:
                sentences = sent_tokenize(re.sub(r'[.]{2,}|"', ' ', section))
                document.sentences += [s for s in sentences if len(s) > 1]

        document.length = len(document.sentences)

        for i in range(document.length):
            document.tokens.append(word_tokenize(document.sentences[i]))
            document.posTrees.append(ParentedTree.fromstring(self.rerankingParser.simple_parse(document.tokens[i])))
            document.posTags.append(document.posTrees[i].pos())
            document.nerTags.append(self.nerParser.tag(document.tokens[i]))
