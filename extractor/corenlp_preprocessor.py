from pycorenlp import StanfordCoreNLP
import os
from extractor.tools import gate_reader
from timeit import default_timer as timer
import nltk


class Preprocessor:

    def __init__(self, host=None):
        """
        Performs all necessary preprocessing

        :param host: the core-nlp host
        """

        if host is None:
            self.cnlp = StanfordCoreNLP("http://localhost:9000")
        else:
            self.cnlp = StanfordCoreNLP(host)

        self.config = {
            'timeout': 500000,
            'annotators': 'tokenize,ssplit,pos,lemma,parse,ner,depparse,mention,coref',
            'tokenize.language': 'English',
            #'parse.type': 'charniak',
            #'parse.executable': '/home/ubuntu/bllip-parser/',
            #'parse.verbose': 'true',
            #'parse.model': './parse-50best.sh',#'~/.local/share/bllipparser/WSJ+Gigaword-v2',
            'outputFormat': 'json'
        }

    def preprocess(self, document):
        """
        Performs all necessary preprocessing

        :param document: Document object to preprocess.
        :return Document: The processed Document object.
        """

        raw = document.get_raw()
        text = ''
        for section in raw:
            text += raw[section]

        annotation = self.cnlp.annotate(text, self.config)

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

if __name__ =="__main__":

    prep = Preprocessor("http://132.230.224.141:9000")
    abs_path = os.path.dirname(os.path.dirname(__file__))
    documents = gate_reader.parse_dir(abs_path + '/data/articles')
    start = timer()
    prep.preprocess(documents[1])
    print(timer() - start)

