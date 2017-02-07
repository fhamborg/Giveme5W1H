import logging
from timeit import default_timer as timer

import editdistance

from extractor.extractors import action_extractor, environment_extractor, cause_extractor
from extractor.five_w_extractor import FiveWExtractor
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
        annotations = document.annotations[question][:level]
        answers = document.questions[question][:level]

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

    # preprocessor expects the location of the sanford-ner.jar and a model to train the ner-parser
    # stanford-ner can be found here: http://nlp.stanford.edu/software/CRF-NER.shtml

    # initialize desired extractors
    extractor_list = [
        action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        cause_extractor.CauseExtractor()
    ]

    extractor = FiveWExtractor(extractor_list)
    documents = gate_reader.parse_dir('../data/articles')
    scores = {'who': [], 'what': [], 'when': [], 'where': [], 'why': []}

    with CSVWriter('../data/results.csv') as writer:
        print("Starting parsing of %i documents " % len(documents))
        for document in documents:
            print("Parsing '%s'..." % document.raw_title)
            start = timer()
            extractor.parse(document)
            print("Parsed '%s' [%is]" % (document.raw_title, (timer() - start)))
            evaluation = cmp_answers(document)
            for question in evaluation:
                scores[question] = evaluation[question]

            writer.save_document(document, 10)

    print(scores)
