import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import *
from bllipparser import RerankingParser
from multiprocessing import Process, Queue, cpu_count
from timeit import default_timer as timer


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
        #         ner.append(self.nerParser.tag(tokens[n]))
        #         trees.append(ParentedTree.fromstring(self.rerankingParser.simple_parse(tokens[n])))
        #         pos.append(trees[n].pos())

        ner = parallel_parse(ner_resolution, self.nerParser, tokens)
        trees = parallel_parse(tree_construction, self.rerankingParser, tokens)
        pos = [tree.pos for tree in trees]

        document.set_tokens(tokens)
        document.set_pos(pos)
        document.set_trees(trees)
        document.set_ner(ner)


def parallel_parse(function, parser, tokens):
    workers = []
    result = [None] * len(tokens)
    q_in = Queue()
    q_out = Queue()

    for i, sentence in enumerate(tokens):
        q_in.put((i, sentence))

    for i in range(cpu_count()):
        worker = Process(target=function, args=(q_in, q_out, parser))
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()

    while not q_out.empty():
        output = q_out.get()
        result[output[0]] = output[1]

    return result


def ner_resolution(q_in, q_out, parser):
    while not q_in.empty():
        arg = q_in.get()
        result = arg[0], parser.tag(arg[1])
        q_out.put(result)


def tree_construction(q_in, q_out, parser):
    while not q_in.empty():
        arg = q_in.get()
        print(arg)
        result = (arg[0], ParentedTree.fromstring(parser.simple_parse(arg[1])))
        q_out.put(result)
