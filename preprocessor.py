import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import *
from bllipparser import RerankingParser
#from bllipparser import Tree


class Preprocessor:
    nerParser = None
    rerankingParser = None


    def __init__(self, classifier, ner):

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
        document.sentences = sent_tokenize(document.raw_title)

        if document.raw_description is not None:
            document.desc_offset = len(document.sentences)
            document.sentences += sent_tokenize(document.raw_description)

        for i in range(len(document.sentences)):
            document.tokens.append(word_tokenize(document.sentences[i]))
            document.posTrees.append(ParentedTree.fromstring(self.rerankingParser.simple_parse(document.tokens[i])))
            document.posTags.append(document.posTrees[i].pos())

            # NER is restricted to the title to reduce the workload
            #if 1000 <= document.desc_offset:
            document.nerTags.append(self.nerParser.tag(document.tokens[i]))

    def labelner(self, tokens):
        return self.nerParser.tag(tokens)
