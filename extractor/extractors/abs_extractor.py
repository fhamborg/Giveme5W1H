import logging
import nltk
from nltk.corpus import wordnet
from abc import ABCMeta, abstractmethod
from itertools import product

try:
    basestring = basestring
except NameError:
    basestring = (str, bytes)


class AbsExtractor:
    """
    AbsExtractor is the abstract every Questionextractor should implement.
    This class provides some general similarity measures as well as a simple named entity parser.
    """

    __metaclass__ = ABCMeta
    weights = None
    wn_corpus = False

    def __init__(self, weights=None):
        """
        Initiates the extractor, weights can be passed to overwrite default settings.

        :param weights: Weights used to evaluate answer candidates.
        """
        if weights is not None:
            self.weights = weights

    @abstractmethod
    def extract(self, document):
        """
        Must be implemented by each Extractor, this method will be executed on every document passed to the FiveWExtractor.

        :param document: The Document object to parse
        :type document: Document

        :return: The parsed Document object
        """

        return document
    
    def _evaluate_candidates(self, document):
        return None
    
    def _distCandidateToAnnotation(self, document):
        return 99999

    def _extract_entities(self, tokens, filter=None, inverted=False, phrase_range=1, groups=None):
        """
        Extract named entities from a list of ner tagged tokens.

        :param tokens: A list of tokens and entity information to be parsed
        :type tokens: [(String, String)]
        :param filter: An optional list of tags that should be ignored:
                       LOCATION, ORGANIZATION, DATE, MONEY, PERSON, PERCENTAGE, TIME
        :type filter: [String]
        :param inverted: Boolean determining if the filter should be inverted.
        :type inverted: Boolean
        :param phrase_range: Allowed distance between two entities of the same type.
        :type phrase_range: Integer
        :param groups: Dictionary containing possible entity groupings.
        :type groups: {String: String}

        :return: A list of tuples containing the tokens and their label
        """

        entity_list = []
        entity = [0, 0, None, None]     #[start, end, type, group]
        words = [t[0] for t in tokens]

        if filter is None:
            # default: extract all entities
            filter = ['O']

        if groups is None:
            groups = {}

        for i, token in enumerate(tokens):
            # check if filter allows mentioned entity type
            if (token[1] in filter) is inverted:
                if token[1] == entity[2] and (i - entity[1]) < phrase_range:
                    # token of same type in allowed range discovered
                    entity[1] = i+1
                elif entity[3] is not None and groups.get(token[1]) == entity[3] and (i - entity[1]) < phrase_range:
                    # hybrid group found
                    entity[1] = i+1
                    entity[2] = entity[3]
                else:
                    # token found which has a different typ or is out of range
                    if entity[1] > 0:
                        entity_list.append((words[entity[0]:entity[1]], entity[2]))
                    entity = [i, i+1, token[1], groups.get(token[1])]

        if entity[1] > 0:
            entity_list.append((words[entity[0]:entity[1]], entity[2]))

        return entity_list

    def _filter_duplicates(self, candidates, exact=True):
        """
        Simple candidate filter that drops duplicates

        :param candidates: List of candidates to parse
        :type candidates: [([String]|[(String, String)], Float)]
        :param exact: If true only exact matches are filtered, false filters based on entailment
        :type exact: Boolean

        :return: The filtered candidate list
        """

        mentioned = []
        filtered = []

        for candidate in candidates:
            if type(candidate[0][0]) == str:
                string = ' '.join(candidate[0]).lower()
            else:
                # tuples containing token and pos
                string = ' '.join([c[0] for c in candidate[0]]).lower()

            new = True
            if exact:
                new = string not in mentioned
            else:
                for member in mentioned:
                    if string in member:
                        new = False
                        break
            if new:
                mentioned.append(string)
                filtered.append(candidate)
        return filtered

    def overlap(self, list_a, list_b, sensitive=False):
        """
        Compares two lists of strings and returns a percentage of overlap.

        :param list_a: List of strings
        :type list_a: String
        :param list_b: List of strings
        :type list_b: String
        :param sensitive: Optional parameter, determines if this comparison is case-sensitive
        :type sensitive: Boolean

        :return: A float representing the percentage of overlap.
        """

        if not sensitive:
            # convert all tokens to lowercase
            list_a = list(map(str.lower, list_a))
            list_b = list(map(str.lower, list_b))

        intersection = [x for x in list_a if x in list_b]
        return len(intersection) / max([len(list_a), len(list_b)])

    def sem_overlap(self, list_a, list_b, pos=None):
        """
        Compares two lists of strings based on semantic similarity using wordnet path distance.

        :param list_a: List of tuples containing tokens and POS-label
        :type list_a: [(String, String)]
        :param list_b: List of tuples containing tokens and POS-label
        :type list_b: [(String, String)]
        :param pos: Optional parameter, filters tokens based on POS-label
        :type pos: String

        :return: A float in [0,1] representing the similarity.
        """

        # check if WordNet corpus was already fetched
        if not self.wn_corpus:
            # fetch WordNet corpus
            log = logging.getLogger('GiveMe5W')
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                log.info('Could not find corpus for WordNet, will now try to download the corpus.')
                nltk.download('wordnet')
            self.wn_corpus = True

        # get desired pos parameter for wordnet
        pos_filter = {'n': 'NN', 'v': 'VB'}.get(pos)

        # fetch synsets for each token
        if pos_filter is not None:
            syn_a = [wordnet.synsets(t[0], pos=pos) for t in list_a if t[1].startswith(pos_filter)]
            syn_b = [wordnet.synsets(t[0], pos=pos) for t in list_b if t[1].startswith(pos_filter)]
        else:
            syn_a = [wordnet.synsets(t[0]) for t in list_a]
            syn_b = [wordnet.synsets(t[0]) for t in list_b]

        # drop tokens without synsets
        syn_a = [syn for syn in syn_a if len(syn) > 0]
        syn_b = [syn for syn in syn_b if len(syn) > 0]

        score = 0
        max_b = [0] * len(syn_b)

        for i in range(len(syn_a)):
            max_a = 0
            for j in range(len(syn_b)):
                sim = max(list((wordnet.path_similarity(a, b) or 0) for a, b in product(syn_a[i], syn_b[j])) or [0])
                max_a = max(sim, max_a)
                max_b[j] = max(max_b[j], sim)

            score += max_a

        score += sum(max_b)
        n = len(syn_a) + len(syn_b)

        if n == 0:
            return 0
        return score / n