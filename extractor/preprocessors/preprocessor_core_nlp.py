import logging

import nltk
from pycorenlp import StanfordCoreNLP


class Preprocessor:
    log = None

    def __init__(self, host=None):
        """
        This preprocessor connects to an CoreNLP server to perform sentence splitting, tokenization, syntactic parsing,
        named entity recognition and coref-resolution on passed documents.

        :param host: the core-nlp host
        """

        self.log = logging.getLogger('GiveMe5W')

        # connect to CoreNLP server
        if host is None:
            self.cnlp = StanfordCoreNLP("http://localhost:9000")
        else:
            self.cnlp = StanfordCoreNLP(host)

        # define basic config and desired processing pipeline
        self.config = {
            'timeout': 500000,
            'annotators': 'tokenize,ssplit,pos,lemma,parse,ner,depparse,mention,coref',
            'tokenize.language': 'English',
            # CoreNLPs charniak-wrapper has some problems ...
            # 'parse.type': 'charniak',
            # 'parse.executable': '/home/ubuntu/bllip-parser/',
            # 'parse.verbose': 'true',
            # 'parse.model': './parse-50best.sh',#'~/.local/share/bllipparser/WSJ+Gigaword-v2',
            'outputFormat': 'json'
        }

        self._token_index = None

    def _link_leaf_to_core_nlp(self, s):

        # this is where the magic happens add there additional information per candidate-part/token/leave
        # char index information is in each nlpToken

        #result = (s, {
        #    'nlpToken': self._tokens[self._token_index]
        #})

        result = {
            'nlpToken': self._tokens[self._token_index]
        }

        self._token_index = self._token_index + 1
        return result

    def preprocess(self, document):
        """
        Send the document to CoreNLP server to execute the necessary preprocessing.

        :param document: Document object to process.
        :type document: Document

        :return Document: The processed Document object.
        """

        annotation = self.cnlp.annotate(document.get_full_text(), self.config)

        if type(annotation) == str:
            print(annotation)
        else:
            document.set_sentences(annotation['sentences'], [], [])

            tree = []
            for sentence in annotation['sentences']:

                # that's a hack to add to every tree leave a the tokens result
                self._token_index = 0
                self._tokens = sentence['tokens']
                sentence_tree = nltk.ParentedTree.fromstring(sentence['parse'], read_leaf=self._link_leaf_to_core_nlp)

                # add a reference to the original data from parsing for this sentence
                sentence_tree.stanfordCoreNLPResult = sentence

                tree.append(sentence_tree)

            document.set_trees(tree)
            document.set_corefs(annotation['corefs'])

            tokens = []
            pos = []
            ner = []

            for sentence in annotation['sentences']:
                s_tokens = []
                s_pos = []
                s_ner = []
                for token in sentence['tokens']:
                    s_tokens.append(token)
                    #s_tokens.append(token['originalText'])
                    s_pos.append((token['originalText'], token['pos']))
                    s_ner.append((token['originalText'], token['ner']))

                tokens.append(s_tokens)
                pos.append(s_pos)
                ner.append(s_ner)

            document.set_tokens(tokens)
            document.set_pos(pos)
            document.set_ner(ner)
            document.set_enhancement('coreNLP', annotation)
            document.is_preprocessed(True)
