import time

from geopy.distance import vincenty
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from itertools import product


"""
    Collection of utility methods    
"""

def cmp_text(annotation, candidate):
    """
    Compare the retrieved answer with the annotation using WordNet path distance.

    :param annotation: The correct Answer
    :type annotation: String
    :param candidate: The retrieved Answer
    :type candidate: [String, String]

    :return: Float
    """

    if annotation is None:
        # annotation is NULL
        return -1
    elif candidate is None:
        # no answer was extracted
        return -2

    # fetch synsets for both answers
    syn_a = [wordnet.synsets(t) for t in word_tokenize(annotation)]
    syn_b = [wordnet.synsets(t[0]) for t in candidate]

    # drop tokens without synsets
    syn_a = [syn for syn in syn_a if len(syn) > 0]
    syn_b = [syn for syn in syn_b if len(syn) > 0]

    if not any(syn_a) or not any(syn_b):
        # no synsets were found for one of the answers!
        return -3

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

    return score / len(syn_a) + len(syn_b)


def cmp_date(annotation, candidate, calendar):
    """
    Compare the retrieved answer with the annotation by calculating the time difference in seconds.

    :param annotation: The correct Answer
    :type annotation: (time.struct_time, Integer)
    :param candidate: The retrieved Answer
    :type candidate: [String]

    :return: Float
    """

    if annotation is None:
        # annotation is NULL
        return -1
    elif candidate is None:
        # no answer was extracted
        return -2

    c_time = calendar.parse(' '.join(candidate))

    if c_time[1] == 0:
        # one of the answers couldn't be parsed
        return -3

    return abs(time.mktime(annotation[0]) - time.mktime(c_time[0]))


def cmp_location(annotation, candidate, geocoder):
    """
    Compare the retrieved answer with the annotation using geocoding and comparing the real world distance.

    :param annotation: The geocoded correct Answer
    :type annotation: Location
    :param candidate: The retrieved Answer
    :type candidate: Sting

    :return: Float
    """

    if annotation is None:
        # annotation is NULL or the annotation could'nt be parsed
        return -1
    elif candidate is None:
        # no answer was extracted
        return -2

    location = geocoder.geocode(candidate)
    if location is None:
        # retrieved answer couldn't be parsed
        return -3

    return vincenty(annotation.point, location.point).kilometers