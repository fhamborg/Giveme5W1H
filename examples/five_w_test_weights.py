import logging
import os
import sys
import time
from timeit import default_timer as timer

import editdistance
from geopy.distance import vincenty

sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
from extractor.extractors import action_extractor, environment_extractor
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
from extractor.tools import gate_reader
from extractor.tools.csv_writer import CSVWriter


def cmp_length(annotation, answer):
    # compares the length of answers and corresponding answers
    if annotation is not None and answer is not None:
        return len(annotation) - len(answer)
    return 0


def cmp_levenshtein(annotation, answer):
    # computes edit distance of answers and corresponding answers
    if annotation is not None and answer is not None:
        return editdistance.eval(annotation, answer)
    return 0


def cmp_fnull(annotation, answer):
    if annotation is not None and answer is None:
        return 1
    return 0


def cmp_fnonnull(annotation, answer):
    if annotation is None and answer is not None:
        return 1
    return 0


def cmp_answers(document, questions=None, level=1):
    scores = {'who': [], 'what': [], 'when': [], 'where': [], 'why': []}

    if questions is None:
        questions = ['who', 'what', 'when', 'where', 'why']

    for question in questions:
        annotations = document.get_annotations()[question][:level]
        answers = document.get_answers()[question][:level]

        annotations.extend([None] * (level - len(annotations)))
        answers.extend([None] * (level - len(answers)))

        for i in range(level):
            if answers[i] is None:
                answer = None
            elif question in ['where', 'when']:
                answer = ' '.join(answers[i][0])
            else:
                answer = ' '.join([token[0] for token in answers[i][0]])  # filter pos

            if annotations[i] is None:
                annotation = None
            else:
                annotation = annotations[i][2]

            score = (
                cmp_fnull(annotation, annotations),
                cmp_fnonnull(annotation, annotations),
                cmp_length(annotation, answer),
                cmp_levenshtein(annotation, answer)
            )

            scores[question].append(score)

    return scores


# This is just a simple example how to use the extractor
if __name__ == '__main__':
    log = logging.Logger('FiveWTest')
    log.setLevel(20)

    abs_path = os.path.dirname(os.path.dirname(__file__))
    documents = gate_reader.parse_dir(abs_path + '/data/articles')

    preprocessor = Preprocessor('http://132.230.224.141:9000')
    for doc in documents:
        preprocessor.preprocess(doc)

    env = environment_extractor.EnvironmentExtractor()
    act = action_extractor.ActionExtractor()
    #cau = cause_extractor.CauseExtractor()

    points = 10
    distances = {
        'where': [[0]*points]*points,
        'when': [[[0] * points] * points] * points
    }

    for doc in documents:
        candidates = {'action': act._extract_candidates(doc)}
        c = env._extract_candidates(doc)
        candidates['where'] = c[0]
        candidates['when'] = c[1]

        annotations = doc.get_annotations()
        for q in annotations:
            if any(annotations[q]):
                annotations[q] = annotations[q][0][2].strip()
            else:
                annotations[q] = None

        if annotations['where'] is not None:
            annotations['where'] = env.geocoder.geocode(annotations['where'])
        if annotations['when'] is not None:
            pub_date = env.calendar.parse(doc.get_date() or '')[0]
            annotations['when'] = time.mktime(env.calendar.parse(annotations['when'] or '', pub_date)[0])

        for i in range(points):  # position
            for j in range(points):  # frequency
                for l in range(points):
                    env.weights = ((i/points, j/points), (i/points, 1 + l/points, 1 - l/points, j/points))

                    # measure distance in meters
                    if annotations['where'] is not None:
                        location = env.geocoder.geocode(' '.join(env._evaluate_locations(doc, candidates['where'])[0][0]))
                        distances['where'] += int(vincenty(annotations['where'].point, location.point).meters)

                    #  measure distance in seconds
                    if annotations['when'] is not None:
                        date = time.mktime(env.calendar.parse(' '.join(env._evaluate_dates(doc, candidates['when'])[0][0]))[0]),
                        distances['when'] += abs(annotations['when'] - date)

                    act.weights = (i/points, j/points, l/points)
                    c = act._evaluate_candidates(doc, candidates['action'])[0]
                    if annotations['who'] is not None:
                        agent = ' '.join([x[0] for x in c[0]])

                    if annotations['what'] is not None:
                        action = ' '.join([x[0] for x in c[1]])

                    if annotations['why'] is not None:
                        continue






    scores = {'who': [], 'what': [], 'when': [], 'where': [], 'why': []}
    count_candidates_total = 0
    start_all = timer()

    with CSVWriter(abs_path + '/data/results.csv') as writer:
        print("Starting parsing of %i documents " % len(documents))
        for document in documents:
            print("Parsing '%s'..." % document.get_title())
            start = timer()
            print("Parsed  '%s' [%is]" % (document.get_title(), (timer() - start)))
            evaluation = cmp_answers(document)
            answers = document.get_answers()
            for question in evaluation:
                scores[question] = evaluation[question]
                print('%s' % question)
                # print('%s' % scores[question].translate(None, "'"))
                print('#candidates: %i' % len(answers[question]))
                count_candidates_total += len(answers[question])

            writer.save_document(document, 10)

    diff_all = timer() - start_all

    print(scores)
    print(count_candidates_total)
    print("candidates/article={}".format(count_candidates_total / len(documents)))
    print("total time={}, time/article={}".format(diff_all, diff_all / len(documents)))
