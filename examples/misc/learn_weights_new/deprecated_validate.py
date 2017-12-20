"""
evaluates the scores for the given documents
"""

import json
import threading

from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler
from extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from misc.learn_weights_new.evaluate import normalize
from misc.learn_weights_new.run import action

_inputPath = path('../examples/datasets/gold_standard/data')
_preprocessedPath = path('../examples/datasets/gold_standard/cache')

if __name__ == '__main__':

    # get a learn instance to use scoring tools
    lock = threading.Lock()
    learn_instance = action(lock)

    inputPath = path(_inputPath)
    preprocessedPath = path(_preprocessedPath)

    # Setup with defaults
    extractor_object = FiveWExtractor(extractors=[
        action_extractor.ActionExtractor(
            weights=[0.7, 0.3, 0]
        ),
        environment_extractor.EnvironmentExtractor(
            # not calculated so far
        ),
        cause_extractor.CauseExtractor(

            weights=[0, 0, 0.1, 0]
        ),
        method_extractor.MethodExtractor(
            weights=[0.9, 0.9, 0.8, 0.2]
        )
    ])

    # Put all together, run it once, get the cached document objects
    documents = (
        # initiate the newsplease file handler with the input directory
        Handler(inputPath)
            # set a path to save an load preprocessed documents
            .set_preprocessed_path(preprocessedPath)
            # limit the the to process documents (nice for development)
            .set_limit(19)
            # add an optional extractor (it would do basically just copying without...)
            .set_extractor(extractor_object)
            # saves all document objects for further programming
            .preload_and_cache_documents()
            # executing it
            .process().get_documents()
    )

    results = []
    # calculate score
    for document in documents:
        result = {}
        annotation = document.get_annotations()
        answers = document.get_answers()
        used_weights = []  # dosent matter here
        question = 'why'
        if question in answers and len(answers[question]) > 0:
            top_answer = answers[question][0].get_parts_as_text()
            learn_instance._cmp_helper_min(learn_instance.cmp_text_ngd, question, top_answer, annotation, used_weights,
                                           result)

        question = 'what'
        if question in answers and len(answers[question]) > 0:
            top_answer = answers[question][0].get_parts_as_text()
            learn_instance._cmp_helper_min(learn_instance.cmp_text_ngd, 'what', top_answer, annotation, used_weights,
                                           result)

        question = 'who'
        if question in answers and len(answers[question]) > 0:
            top_answer = answers[question][0].get_parts_as_text()
            learn_instance._cmp_helper_min(learn_instance.cmp_text_ngd, question, top_answer, annotation, used_weights,
                                           result)

        question = 'how'
        if question in answers and len(answers[question]) > 0:
            top_answer = answers[question][0].get_parts_as_text()
            learn_instance._cmp_helper_min(learn_instance.cmp_text_ngd, question, top_answer, annotation, used_weights,
                                           result)

        question = 'when'
        if question in answers and len(answers[question]) > 0:
            top_answer = answers[question][0].get_enhancement('timex')
            learn_instance._cmp_helper_min(learn_instance.cmp_date_timex, question, top_answer, annotation,
                                           used_weights, result)

        question = 'where'
        if question in answers and len(answers[question]) > 0:
            top_answer = answers[question][0].get_parts_as_text()
            learn_instance._cmp_helper_min(learn_instance.cmp_location, question, top_answer, annotation, used_weights,
                                           result)
        results.append(result)

    # write raw results
    with open('result/VALIDATION.json', 'w') as data_file:
        data_file.write(json.dumps(results, sort_keys=False, indent=4))
        data_file.close()

    result_avg = {}
    for result in results:
        for question in result:
            avg_question = result_avg.setdefault(question, [])
            avg_question.append(result[question][2])

    for result_avg_question in result_avg:
        scores_norm = normalize(result_avg[result_avg_question])
        a_sum = sum(scores_norm)
        result_avg[result_avg_question] = a_sum / len(scores_norm)

    # write raw results
    with open('result/VALIDATION_AVG.json', 'w') as data_file:
        data_file.write(json.dumps(result_avg, sort_keys=False, indent=4))
        data_file.close()
