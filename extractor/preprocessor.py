import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import *
from bllipparser import RerankingParser


class Preprocessor:
    nerParser = None
    rerankingParser = None

    def __init__(self, tagger, model):
        """
        Performs all necessary preprocessing

        :param tagger: Path to the Stanford NER Tagger
        :param model: Path to the model for the NER Tagger
        """

        # check if model for tokenizer exists
        try:
            nltk.data.find('punkt.zip')
        except:
            nltk.download('punkt')

        # init NER parser
        self.nerParser = StanfordNERTagger(tagger, model)

        # init Charniak parser
        self.rerankingParser = RerankingParser.fetch_and_load('WSJ+Gigaword-v2')

    def preprocess(self, document):
        """
        Performs all necessary preprocessing

        :param document: Document object to preprocess.
        :return Document: The processed Document object.
        """

        raw = document.get_raw()
        sections = []
        tokens = []
        pos = []
        trees = []
        ner = []


        for section in raw:
            # delete '...' and quotes from plain text, then split sentences
            sentences = sent_tokenize(re.sub(r'[.]{2,}|"', ' ', raw[section]))
            # cut sentences with more than 398 tokens
            sections.append([s[:398] for s in sentences if len(s) > 1])

        document.set_sentences(sections[0], sections[1], sections[2])

        for section in sections:
            for sentence in section:
                n = len(tokens)
                tokens.append(word_tokenize(sentence))
                ner.append(self.nerParser.tag(tokens[n]))
                trees.append(ParentedTree.fromstring(self.rerankingParser.simple_parse(tokens[n])))
                pos.append(trees[n].pos())

        document.set_tokens(tokens)
        document.set_pos(pos)
        document.set_trees(trees)
        document.set_ner(ner)
