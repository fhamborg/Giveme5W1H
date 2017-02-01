from abc import ABCMeta, abstractmethod

try:
    basestring = basestring
except NameError:
    basestring = (str, bytes)

"""Abstract class for answer extractors.
"""


class AbsExtractor:
    __metaclass__ = ABCMeta
    overwrite = True

    def __init__(self, overwrite=True):
        """
        :param overwrite: determines if existing answers should be overwritten.
        """
        self.overwrite = overwrite

    @abstractmethod
    def extract(self, document):
        return document

    def answer(self, document, question, answer):
        """
        Saves a certain answer for a document.

        :param document: The Document that is processed.
        :param question: The question that is answered.
        :param answer: The actual answer.
        :return:
        """
        if self.overwrite or len(document.questions[question]) == 0:
            document.questions[question] = answer
        else:
            prev_answer = document.questions[question]
            if isinstance(prev_answer, basestring):
                prev_answer = [prev_answer, answer]
            else:
                prev_answer.append(answer)
            document.questions[question] = prev_answer

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