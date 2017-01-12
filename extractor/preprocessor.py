import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import *
from bllipparser import RerankingParser


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
        length = 0
        for section in [document.raw_title, document.raw_description, document.raw_text]:
            document.section_offsets.append(length)
            if section is not None:
                sentences = sent_tokenize(section)
                document.sentences += [s.replace('"', '') for s in sentences]
                length += len(sentences)

        document.length = length

        for i in range(length):
            document.tokens.append(word_tokenize(document.sentences[i]))
            document.posTrees.append(ParentedTree.fromstring(self.rerankingParser.simple_parse(document.tokens[i])))
            document.posTags.append(document.posTrees[i].pos())
            if i < document.section_offsets[2]:
                document.nerTags.append(self.nerParser.tag(document.tokens[i]))
