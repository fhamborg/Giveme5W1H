"""
    Collection of utility methods    
"""


def bytes_2_human_readable(number_of_bytes):
    """
    converts bytes to a readable formatted string
    :param number_of_bytes:
    :return:
    """
    if number_of_bytes < 0:
        raise ValueError("!!! numberOfBytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit

#
#
# def cmp_text(annotation, candidate):
#     """
#     Compare the retrieved answer with the annotation using WordNet path distance.
#
#     :param annotation: The correct Answer
#     :type annotation: String
#     :param candidate: The retrieved Answer
#     :type candidate: [String, String]
#
#     :return: Float
#     """
#
#     if annotation is None or annotation is 'NULL':
#         # annotation is NULL
#         return -1
#     elif candidate is None:
#         # no answer was extracted
#         return -2
#
#     # fetch synsets for both answers
#     syn_a = [wordnet.synsets(t) for t in word_tokenize(annotation)]
#     syn_b = [wordnet.synsets(t[0]) for t in candidate]
#
#     # drop tokens without synsets
#     syn_a = [syn for syn in syn_a if len(syn) > 0]
#     syn_b = [syn for syn in syn_b if len(syn) > 0]
#
#     if not any(syn_a) or not any(syn_b):
#         # no synsets were found for one of the answers!
#         return -3
#
#     score = 0
#     max_b = [0] * len(syn_b)
#
#     for i in range(len(syn_a)):
#         max_a = 0
#         for j in range(len(syn_b)):
#             sim = max(list((wordnet.path_similarity(a, b) or 0) for a, b in product(syn_a[i], syn_b[j])) or [0])
#             max_a = max(sim, max_a)
#             max_b[j] = max(max_b[j], sim)
#
#         score += max_a
#     score += sum(max_b)
#
#     return score / len(syn_a) + len(syn_b)
#
#
# def cmp_date(annotation, candidate, calendar):
#     """
#     Compare the retrieved answer with the annotation by calculating the time difference in seconds.
#
#     "Beide Datum - das kleiner datum das genau in der mitte liegt -
#     "Datum in der mitten nutzen
#     "Datum, die Zeit Reibschreibe?
#
#     :param annotation: The correct Answer
#     :type annotation: (time.struct_time, Integer)
#     :param candidate: The retrieved Answer
#     :type candidate: [String]
#
#     :return: Float
#     """
#
#     t = calendar.parse(annotation)
#     if t[1] == 0:
#         return -1
#
#     elif candidate is None:
#         # no answer was extracted
#         return -2
#
#     strings = []
#     for candidatepart in candidate:
#         strings.append(candidatepart[0])
#
#     c_time = calendar.parse(' '.join(strings))
#
#     if c_time[1] == 0:
#         # one of the answers couldn't be parsed
#         return -3
#
#     a = time.mktime(t[0])
#     b = time.mktime(c_time[0])
#     return abs(a - b)
#
#
# def cmp_location(annotation, candidate, geocoder):
#     """
#     Compare the retrieved answer with the annotation using geocoding and comparing the real world distance.
#
#     :param annotation: The geocoded correct Answer
#     :type annotation: Location
#     :param candidate: The retrieved Answer
#     :type candidate: Sting
#
#     :return: Float
#     """
#
#     if annotation is None:
#         # annotation is NULL or the annotation could'nt be parsed
#         return -1
#     elif candidate is None:
#         # no answer was extracted
#         return -2
#
#     location = geocoder.geocode(candidate)
#     if location is None:
#         # retrieved answer couldn't be parsed
#         return -3
#
#     return vincenty(annotation.point, location.point).kilometers
