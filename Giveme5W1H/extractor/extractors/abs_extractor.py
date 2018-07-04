import logging
import warnings
from abc import ABCMeta, abstractmethod
from itertools import product

import nltk
from nltk.corpus import wordnet

from Giveme5W1H.extractor.candidate import Candidate
from Giveme5W1H.extractor.document import Document


class AbsExtractor:
    """
    AbsExtractor is the abstract every Questionextractor should implement.
    This class provides some general similarity measures as well as a simple named entity parser.
    """

    __metaclass__ = ABCMeta
    wn_corpus = False

    @abstractmethod
    def _extract_candidates(self, document):
        pass

    @abstractmethod
    def _evaluate_candidates(self, document):
        pass

    def process(self, document: Document):
        """
        Must be implemented by each Extractor, this method will be executed on every document passed to the MasterExtractor.

        :param document: The Document object to parse
        :type document: Document

        :return: None, verything it store within the document object (set_candiadates)
        """
        if not document.has_candidates(self.get_id()):
            self._extract_candidates(document)
        self._evaluate_candidates(document)
        return

    def get_id(self):
        """
        returns name of the class as string
        :return:
        """
        return str(self.__class__.__name__)

    def _extract_entities(self, tokens, filter=None, inverted=False, phrase_range=1, groups=None, accessor='ner'):
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
        # entity_list_tmp = []
        entity = [0, 0, None, None]  # [start, end, type, group]
        # words = [t['originalText'] for t in tokens]

        if filter is None:
            # default: extract all entities
            filter = ['O']

        if groups is None:
            groups = {}

        for i, token in enumerate(tokens):
            tag = token[accessor]
            # check if filter allows mentioned entity type
            if (tag in filter) is inverted:
                if tag == entity[2] and (i - entity[1]) < phrase_range:
                    # token of same type in allowed range discovered
                    entity[1] = i + 1
                elif entity[3] is not None and groups.get(tag) == entity[3] and (i - entity[1]) < phrase_range:
                    # hybrid group found
                    entity[1] = i + 1
                    entity[2] = entity[3]
                else:
                    # token found which has a different typ or is out of range
                    if entity[1] > 0:
                        entity_list.append((tokens[entity[0]:entity[1]], entity[2]))
                        # entity_list_tmp.append((words[entity[0]:entity[1]], entity[2]))
                    entity = [i, i + 1, tag, groups.get(tag)]

        if entity[1] > 0:
            entity_list.append((tokens[entity[0]:entity[1]], entity[2]))
            # entity_list_tmp.append((words[entity[0]:entity[1]], entity[2]))

        return entity_list


    def _filter_candidate_dublicates(self, candidates):
        """
        Candidate filter that drops duplicates based on string match.
        The first candidate int the list is taken
        :param candidates:
        :return:
        """
        unique_map = {}
        unique_candidates = []
        for candidate in candidates:
            text = candidate.get_parts_as_text()
            text_id = ''.join(e for e in text if e.isalnum())
            if unique_map.get(text_id):
                # skip this one
                continue
            else:
                unique_candidates.append(candidate)
                unique_map[text_id] = True

        return  unique_candidates


    def _filter_duplicates(self, candidates, exact=True):
        """
        Simple candidate filter that drops duplicates

        :param candidates: List of candidates to parse
        :type candidates: [([String]|  [(String, String)], Float)]
        :param exact: If true only exact matches are filtered, false filters based on entailment
        :type exact: Boolean

        :return: The filtered candidate list

        """

        mentioned = []
        filtered = []

        for candidate in candidates:

            string_a = []
            for part in candidate[0]:
                string_a.append(part[0]['nlpToken']['lemma'])
            string = ' '.join(string_a)

            if exact:
                new = string not in mentioned
            else:
                for member in mentioned:
                    if string in member:
                        new = False
                        break

            mentioned.append(string)

            cd = Candidate()
            cd.set_parts(candidate[0])
            cd.set_score(candidate[1])
            cd.set_sentence_index(candidate[2] if 2 < len(candidate) else None)
            cd.set_type(candidate[3] if 3 < len(candidate) else None)

            # cd.set_text_index(text_index)

            filtered.append(cd)

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

    def _pos_linked_to_corenlp_tokens(self, tree):
        """
        Most of the extractor work with a tree structure and don`t save any backlink to the original text or
        the core NLP results.

        This method can take a (sub)-tree/leave and walk back the tree and count all left hand-nodes.
        By doing so it is possible to extract all Core-NLP-Information for the candidates and their tokens.
        """
        warnings.warn(
            "There should be no need for this function anymore, use instead the information within the leave",
            DeprecationWarning
        )

        root = tree.root()
        pos = tree.pos()
        candidate_parts_as_list = []
        start_index = self.__find_index_from_root(tree.root(), list(tree.treeposition())) - 1

        posLen = len(pos)

        # TODO
        # bugfix, at some very rare occasion the tree isn`t exactly reflecting the CoreNLP structure
        if posLen + start_index >= len(root.stanfordCoreNLPResult['tokens']):
            posLen = len(root.stanfordCoreNLPResult['tokens']) - start_index - 1

        for x in range(0, posLen):
            # convert part tuple to list, get token
            token = root.stanfordCoreNLPResult['tokens'][x + start_index]
            parts_as_list = list(pos[x])
            parts_as_list.append(token)
            # save list core_nlp result in the list
            candidate_parts_as_list.append(parts_as_list)

        return [tuple(x) for x in candidate_parts_as_list]

    def _count_elements(self, root):
        """
        returns the leave count of tree
        :param root:
        :return:
        """
        count = 0
        if isinstance(root, list):
            for element in root:
                if isinstance(element, list):
                    count += self._count_elements(element)
                else:
                    count += 1
        else:
            count += 1
        return count

    def __find_index_from_root(self, root, path):
        """
        finds the index position
        :param root:
        :param path:
        :return:
        """
        if (len(path) > 1):
            position = path.pop(0)
            leftChildCount = 0
            for x in range(0, position):
                leftChildCount = leftChildCount + self._count_elements(root[x])
            return leftChildCount + self.__find_index_from_root(root[position], path)
        elif (len(path) is 1):
            return path.pop(0) + 1
        else:
            return 0
