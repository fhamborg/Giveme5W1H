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
            #'parse.type': 'charniak',
            #'parse.executable': '/home/ubuntu/bllip-parser/',
            #'parse.verbose': 'true',
            #'parse.model': './parse-50best.sh',#'~/.local/share/bllipparser/WSJ+Gigaword-v2',
            'outputFormat': 'json'
        }

    def preprocess(self, document):
        """
        Send the document to CoreNLP server to execute the necessary preprocessing.

        :param document: Document object to process.
        :type document: Document

        :return Document: The processed Document object.
        """

        annotation = self.cnlp.annotate(document.get_fullText(), self.config)
        

        if type(annotation) == str:
            print(annotation)
        else:
            document.set_sentences(annotation['sentences'], [], [])
            document.set_trees([nltk.ParentedTree.fromstring(sentence['parse']) for sentence in annotation['sentences']])
            document.set_corefs(annotation['corefs'])

            tokens = []
            pos = []
            ner = []

            for sentence in annotation['sentences']:
                s_tokens = []
                s_pos = []
                s_ner = []
                for token in sentence['tokens']:
                    s_tokens.append(token['originalText'])
                    s_pos.append((token['originalText'], token['pos']))
                    s_ner.append((token['originalText'], token['ner']))

                tokens.append(s_tokens)
                pos.append(s_pos)
                ner.append(s_ner)

            document.set_tokens(tokens)
            document.set_pos(pos)
            document.set_ner(ner)
            document.set_clp_result(annotation)
            document.is_preprocessed(True)
            
