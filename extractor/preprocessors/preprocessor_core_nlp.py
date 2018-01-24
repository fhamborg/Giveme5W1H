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

        # define basic base_config and desired processing pipeline
        self.base_config = {
            'timeout': 500000,
            'annotators': 'tokenize,ssplit,pos,lemma,parse,ner,depparse,mention,coref',
            'tokenize.language': 'English',
            # 'coref.algorithm' :'neural', see https://github.com/smilli/py-corenlp/issues/18
            # CoreNLPs charniak-wrapper has some problems ...
            # 'parse.type': 'charniak',
            # 'parse.executable': '/home/ubuntu/bllip-parser/',
            # 'parse.verbose': 'true',
            # 'parse.model': './parse-50best.sh',#'~/.local/share/bllipparser/WSJ+Gigaword-v2',
            'outputFormat': 'json'
        }

        self._token_index = None

    def _link_leaf_to_core_nlp(self, s):
        """
        this is where the magic happens add there additional information per candidate-part/token/leave
        char index information is in each nlpToken
        """
        if len(self._tokens) - 1 < self._token_index:
            # there seams a bug around numbers,
            # spitted numbers in the same token are called as they have been split to different tokens
            # this leads to a wrong index, everything in this sentence is lost till the end of that sentence
            self.log.error('fix the doc around(reformat number,remove special characters):' + s)
            # print the last two tokens to make it spotable
            self.log.error(self._tokens[-1])
            self.log.error(self._tokens[-2])

            # further we can`t return None because this would break extractors
            # therefore we use this bugfix object
            # TODO: reason if it make sense to reject these documents at all, because result isn`t reliable at all
            # TODO: flag document at least with some error flags
            result = {
                'nlpToken': {
                    'index': 7,
                    'word': 'BUGFIX',
                    'originalText': 'BUGFIX',
                    'lemma': 'BUGFIX',
                    'characterOffsetBegin': 0,
                    'characterOffsetEnd': 0,
                    'pos': 'BUGFIX',
                    'ner': 'BUGFIX',
                    'speaker': 'BUGFIX',
                    'before': ' ',
                    'after': ''
                }
            }

            if self._document:
                self._document.set_error_flag('core_nlp')


        else:
            result = {
                'nlpToken': self._tokens[self._token_index]
            }

        self._token_index = self._token_index + 1

        return result

    def _build_actual_config(self, document):
        """
        Creates the actual config, consisting of the base_config and dynamic_params. if the same key exists in both
        base_config and dynamic_params, the value will be used from dynamic_params, i.e., base_config will be overwritten.
        :param document:
        :return:
        """
        dynamic_config = {
            'date': document.get_date()
        }
        actual_config = {**self.base_config, **dynamic_config}
        return actual_config

    def preprocess(self, document):
        """
        Send the document to CoreNLP server to execute the necessary preprocessing.

        :param document: Document object to process.
        :type document: Document

        :return Document: The processed Document object.
        """
        actual_config = self._build_actual_config(document)
        annotation = self.cnlp.annotate(document.get_full_text(), actual_config)

        if type(annotation) is str:
            print(annotation)
        else:
            document.set_sentences(annotation['sentences'], [], [])
            self._document = document

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
