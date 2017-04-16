import logging
import re
import nltk
from nltk.tree import ParentedTree
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from bllipparser import RerankingParser
from multiprocessing import Process, Queue, cpu_count


class Preprocessor:
    """
    This preprocessor uses the nltk library, the Stanford NER tagger as well the Bllip parser to perform
    sentence splitting, tokenization, syntactic parsing and named entity recognition on passed documents.
    """

    log = None
    nerParser = None
    rerankingParser = None

    def __init__(self, ner_tagger, ner_model=None):
        """
        Initializes the preprocessor by loading all necessary models.

        :param ner_tagger: Absolute path to the Stanford NER jar
        :type ner_tagger: String
        :param ner_model: Absolute path to the model used by the NER tagger (optional)
        :type ner_model: String
        """

        self.log = logging.getLogger('GiveMe5W')

        # fetch model used for tokenization
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            self.log.info('Could not find model for tokenizer, will now try to download the model.')
            nltk.download('punkt')

        # init NER parser
        if ner_model is None:
            # set default model for ner tagger
            import os
            ner_model = os.path.dirname(ner_tagger) + '/classifiers/english.muc.7class.distsim.crf.ser.gz'
        self.nerParser = StanfordNERTagger(ner_model, ner_tagger)
        self.log.debug('StanfordNERTagger initialized!')

        # init Charniak parser
        self.rerankingParser = RerankingParser.fetch_and_load('WSJ+Gigaword-v2')
        self.log.debug('Charniak RerankingParser initialized!')

    def preprocess(self, document):
        """
        Perform sentence splitting, tokenization, syntactic parsing and named entity recognition on passed document.

        :param document: Document object to process.
        :type document: Document

        :return Document: The processed Document object.
        """

        raw = document.get_raw()
        sections = []
        tokens = []

        # first split sentences and remove constructs like '...' or quotes from the text
        # second shorten sentences with more than 398 tokens to avoid exceptions by reranking parser
        for section in raw:
            sentences = sent_tokenize(re.sub(r'[.]{2,}|"', ' ', raw[section]))

            for index, sentence in enumerate(sentences):
                if len(sentence) > 398:
                    self.log.debug('Preprocessor: Sentence cut after 398 characters:\n%s' % sentence)
                    sentences[index] = sentence[:398]

            sections.append(sentences)

        document.set_sentences(sections[0], sections[1], sections[2])
        self.log.debug('Preprocessor: Finished splitting sentences, %i sentences found.' % document.get_len())

        # tokenize sentences
        for section in sections:
            for sentence in section:
                tokens.append(word_tokenize(sentence))

        # parallel named entity recognition and syntactic parsing
        ner = parallel_parse(ner_resolution, self.nerParser, tokens)
        self.log.debug('Preprocessor: Finished NER resolution.')
        trees = parallel_parse(tree_construction, self.rerankingParser, tokens)
        self.log.debug('Preprocessor: Finished syntactic parsing.')

        # extract pos labels from syntactic parsing
        pos = [tree.pos() for tree in trees]

        # store variables in document
        document.set_tokens(tokens)
        document.set_pos(pos)
        document.set_trees(trees)
        document.set_ner(ner)
        self.log.info("Preprocessor: Finished preprocessing: '%s...'" % document.get_title()[:25])



def parallel_parse(function, parser, sentences):
    """
    Distributes sentences of a document to set of workers for parsing.

    :param function: Function to perform on the sentences
    :param parser: The parser necessary for the function
    :type parser: StanfordNERTagger | RerankingParser
    :param sentences: Sentences that should be parsed
    :type sentences:

    :return: List of results from the parsing function
    """

    workers = []
    result = [None] * len(sentences)

    # queues used to communicate with workers
    q_in = Queue()      # open jobs
    q_out = Queue()     # results from workers

    # initiate workers based on cpu-count
    for i in range(cpu_count()):
        worker = Process(target=function, args=(q_in, q_out, parser))
        worker.start()
        workers.append(worker)

    # number of distributed and retrieved tasks
    pushed = 0
    retrieved = 0
    while True:
        if pushed < len(sentences):
            # there are still unprocessed sentences to push into the queue
            q_in.put((pushed, sentences[pushed]))
            pushed += 1
        elif pushed == len(sentences):
            # all sentences were pushed, push terminating None for each worker
            for worker in workers:
                q_in.put(None)
                pushed += 1

        if retrieved < len(sentences) and (pushed - retrieved > len(workers) or pushed >= len(sentences)):
            # only wait for results if enough jobs are in the input queue
            output = q_out.get()
            result[output[0]] = output[1]
            retrieved += 1
        elif retrieved == len(sentences):
            # all jobs are finished
            break

    # wait for workers to terminate
    for worker in workers:
        worker.join()

    return result


def ner_resolution(q_in, q_out, parser):
    """
    Function for a parallel_parse-worker, this function performs NER resolution on sentences

    :param q_in: Queue containing open jobs
    :type q_in: Queue
    :param q_out: Queue used to return results
    :type q_out: Queue
    :param parser: Parse used to process a sentence
    :type parser: StanfordNERTagger

    :return: None
    """

    while True:
        # wait for sentence
        arg = q_in.get()
        if arg is None:
            #  termination signal received
            break
        else:
            # parse sentence and return
            q_out.put((arg[0], parser.tag(arg[1])))


def tree_construction(q_in, q_out, parser):
    """
    Function for a parallel_parse-worker, this function performs syntactic parsing on sentences

    :param q_in: Queue containing open jobs
    :type q_in: Queue
    :param q_out: Queue used to return results
    :type q_out: Queue
    :param parser: Parse used to process a sentence
    :type parser: RerankingParser

    :return: None
    """

    while True:
        arg = q_in.get()
        if arg is None:
            #  termination signal received
            break
        else:
            # parse sentence and return
            q_out.put((arg[0], ParentedTree.fromstring(parser.simple_parse(arg[1]))))
