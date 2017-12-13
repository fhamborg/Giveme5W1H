"""
checks all result files an writes the best candidates to evaluate.json
"""
import glob
import json
import pickle

import statistics


def normalize(question, data):
    pass


def weights_to_string(weights):
    scaled_weights_string = [str(x) for x in weights]
    return ''.join(scaled_weights_string)


def stats(numbers):
    return {"mean": statistics.mean(numbers),
            "median": statistics.median(numbers)}


def read_file(path):
    # filename = os.path.basename(file_path)
    score_results = {}
    for file_path in glob.glob(path):
        with open(file_path, 'rb') as ff:
            results = pickle.load(ff)
        for result in results:
            for question in result:
                question_scores = score_results.setdefault(question, {})
                weights = result[question][1]

                comb = question_scores.setdefault(weights_to_string(weights), {'weights': weights, 'scores_doc': []})
                comb['scores_doc'].append(result[question][2])
    return score_results


def remove_errors(list):
    return [x for x in list if x and x >= 0]


def index_of_best(list):
    """

    :param list:
    :return:
    """
    a_list = remove_errors(list)
    return list.index(min(a_list))


if __name__ == '__main__':

    # read all available prickles
    score_results = read_file('queue_caches/*processed.prickle')

    # write raw results
    with open('result/evaluation_full' + '.json', 'w') as data_file:
        data_file.write(json.dumps(score_results, sort_keys=False, indent=4))
        data_file.close()

    #
    # 1. Crit.: has a low dist on average per weight (documents are merged)
    # 3. Crit.: weight with lowest error rate per documents (documents are merged)
    score_per_average = {}
    results_error_rate = {}
    for question in score_results:
        for combination_string in score_results[question]:
            combo = score_results[question][combination_string]

            scores_cleaned = remove_errors(combo['scores_doc'])
            errors = len(combo['scores_doc']) - len(scores_cleaned)
            a_sum = sum(scores_cleaned)

            combo['avg'] = a_sum / len(scores_cleaned)
            score_per_average.setdefault(question,{})[combination_string] = {
                'score': a_sum,
                'avg': combo['avg'],
                'weight': combo['weights']
            }

            results_error_rate.setdefault(question,{})[combination_string] = {
                'errors': errors,
                'weight': combo['weights']
            }

    for question in results_error_rate:
        print(question)
        results_error_rate_list = list(results_error_rate[question].values())
        score_per_average_list = list(score_per_average[question].values())

        results_error_rate_list.sort(key=lambda x: x['errors'], reverse=False)
        score_per_average_list.sort(key=lambda x: x['avg'], reverse=False)

        print('lowest error rate:')
        print(json.dumps(results_error_rate_list[:30], sort_keys=False, indent=4))

        print('best scoring weights:')
        print(json.dumps(score_per_average_list[:30], sort_keys=False, indent=4))

    # nice formattet full output, if anyone need is
    nice_format = {}
    for question in score_results:
        question_scores = nice_format.setdefault(question, [])
        for combination_string in score_results[question]:
            combo = score_results[question][combination_string]
            del combo['scores_doc']
            question_scores.append(combo)

    with open('result/evaluation_only_avg' + '.json', 'w') as data_file:
        data_file.write(json.dumps(nice_format, sort_keys=False, indent=4))
        data_file.close()
