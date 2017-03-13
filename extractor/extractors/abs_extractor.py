from abc import ABCMeta, abstractmethod
from itertools import product
from nltk.corpus import wordnet

try:
    basestring = basestring
except NameError:
    basestring = (str, bytes)

"""Abstract class for answer extractors.
"""


class AbsExtractor:
    __metaclass__ = ABCMeta
    overwrite = True
    weights = None

    def __init__(self, weights=None, overwrite=True):
        """
        :param overwrite: determines if existing answers should be overwritten.
        """
        if weights is not None:
            self.weights = weights

        self.overwrite = overwrite

    @abstractmethod
    def extract(self, document):
        return document

    # def answer(self, document, question, answer):
    #     """
    #     Saves a certain answer for a document.
    #
    #     :param document: The Document that is processed.
    #     :param question: The question that is answered.
    #     :param answer: The actual answer.
    #     :return:
    #     """
    #     if self.overwrite or len(document.questions[question]) == 0:
    #         document.questions[question] = answer
    #     else:
    #         prev_answer = document.questions[question]
    #         if isinstance(prev_answer, basestring):
    #             prev_answer = [prev_answer, answer]
    #         else:
    #             prev_answer.append(answer)
    #         document.questions[question] = prev_answer

    def _extract_entities(self, tokens, filter=None, inverted=False, phrase_range=1, groups=None):
        """
        Extract named entities from ner tagged list of tokens.

        :param tokens: A list of tokens and entity information to be parsed
        :param filter: An optional list of tags that should be ignored:
                       LOCATION, ORGANIZATION, DATE, MONEY, PERSON, PERCENTAGE, TIME
        :param inverted: Boolean determining if the filter should be inverted.
        :param phrase_range: Allowed distance between two entities of the same type.
        :param groups: Dictionary containing possible entity groupings.
        :return: A list of tuples containing the tokens and their label
        """

        entity_list = []
        entity = [0, 0, None, None]
        words = [t[0] for t in tokens]

        if filter is None:
            filter = ['O']

        if groups is None:
            groups = {}

        for i in range(len(tokens)):
            token = tokens[i]

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
        :param list_b: List of strings
        :param sensitive: Optional parameter, determines if this comparison is case-sensitive
        :return: A float representing the percentage of overlap.
        """

        if not sensitive:
            list_a = list(map(str.lower, list_a))
            list_b = list(map(str.lower, list_b))

        intersection = [x for x in list_a if x in list_b]
        return len(intersection) / max([len(list_a), len(list_b)])

    def sem_overlap(self, list_a, list_b, pos=None):
        """
        Compares two lists of strings based on semantic similarity.

        :param list_a: List of tuples containing tokens and POS-label
        :param list_b: List of tuples containing tokens and POS-label
        :param pos: Optional parameter, filters tokens based on POS-label
        :return: A float representing the similarity.
        """

        pos_filter = {'n': 'NN', 'v': 'VB'}.get(pos)
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