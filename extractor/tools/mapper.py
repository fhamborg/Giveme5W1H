"""
Helper to get relation to extractors, questions and their weights
"""


def weight_to_string(extractor, weight_index, question: str = None):
    """
    naming for a weight
    :param extractor:
    :param weight_index:
    :return:
    """
    if extractor == 'action':
        if weight_index == 0:
            return 'position'
        elif weight_index == 1:
            return 'frequency'
        elif weight_index == 2:
            return 'named_entity'
    elif extractor == 'cause':
        if weight_index == 0:
            return 'position'
        elif weight_index == 1:
            return 'clausal conjunction'
        elif weight_index == 2:
            return 'adverbial indicator'
        elif weight_index == 3:
            return 'NP-VP-NP'
    elif extractor == 'environment':
        if question.startswith('where'):
            if weight_index == 0:
                return 'position'
            elif weight_index == 1:
                return 'frequency'
            elif weight_index == 2:
                return 'entailment'
            elif weight_index == 3:
                return 'accurate'
        if question.startswith('when'):
            if weight_index == 0:
                return 'position'
            elif weight_index == 1:
                return 'frequency'
            elif weight_index == 2:
                return 'entailment'
            elif weight_index == 3:
                return 'distance_from_publisher_date'
            elif weight_index == 4:
                return 'accurate'
    elif extractor == 'method':
        if weight_index == 0:
            return 'position'
        elif weight_index == 1:
            return 'frequency'
        elif weight_index == 2:
            return 'conjunction'
        elif weight_index == 3:
            return 'adjectives_adverbs'
    else:
        return 'no_mapping'


def question_to_extractor(question: str):
    """
    extractor for a given question
    :param question:
    :return:
    """
    if question == 'who' or question == 'what':
        return 'action'
    elif question == 'why':
        return 'cause'
    elif question == 'where' or question == 'when':
        return 'environment'
    elif question == 'how':
        return 'method'
    else:
        return 'no_mapping'


def extractor_to_question(extractor: str):
    """
    return questions for a extractor in a tuple
    :param extractor:
    :return:
    """
    if extractor == 'action':
        return ('who', 'what')
    elif extractor == 'cause':
        return ('why',)
    elif extractor == 'environment':
        return ('where', 'when')
    elif extractor == 'method':
        return ('how',)
    else:
        return ('no_mapping',)
