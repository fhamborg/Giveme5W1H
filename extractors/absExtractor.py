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

    def __init__(self, overwrite=None):
        if overwrite is not None:
            self.overwrite = overwrite

    @abstractmethod
    def extract(self, document):
        return document

    def answer(self, document, question, answer):
        if self.overwrite or len(document.questions[question]) == 0:
            document.questions[question] = answer
        else:
            prev_answer = document.questions[question]
            if isinstance(prev_answer, basestring):
                prev_answer = [prev_answer, answer]
            else:
                prev_answer.append(answer)
            document.questions[question] = prev_answer

    def _extract_entities(self, tokens, filter=None, inverted=False):
        """
        Extract named entities from ner tagged list of tokens.

        :param tokens: A list of tokens to be parsed
        :param filter: An optional list of tags that should be ignored:
                       LOCATION, ORGANIZATION, DATE, MONEY, PERSON, PERCENTAGE, TIME
        :param inverted: Boolean determining if the filter should be inverted.
        :return: A list of tuples containing the tokens and their label
        """

        entity_list = []
        entity = None

        if filter is None:
            filter = ['O']

        for token in tokens:
            if (token[1] in filter) is inverted:
                if entity is None:
                    entity = [token[0]], token[1]
                elif token[1] == entity[1]:
                    entity[0].append(token[0])
                else:
                    entity_list.append(entity)
                    entity = [token[0]], token[1]
            elif entity is not None:
                entity_list.append(entity)
                entity = None

        if entity is not None:
            entity_list.append(entity)

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