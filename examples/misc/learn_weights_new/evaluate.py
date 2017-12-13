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

                comb = question_scores.setdefault(weights_to_string(weights), {'weights': weights, 'scores': []})
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
            errors = remove_errors(combo['scores_doc']) - len(scores_cleaned)
            a_sum = sum(scores_cleaned)

            combo['avg'] = a_sum / len(scores_cleaned)
            score_per_average[combination_string] = {
                'score': a_sum
            }

            results_error_rate[combination_string] = {
                'errors': errors
            }

    # convert to list...
    results_error_rate = list(results_error_rate.values())
    score_per_average = list(score_per_average.values())
    # ...and sort
    results_error_rate.sort(key=lambda x: x['avg'], reverse=True)
    score_per_average.sort(key=lambda x: x['avg'], reverse=True)

    print('best scoring weights:')
    print(score_per_average[:10])
    print('lowest error rate:')
    print(results_error_rate[:10])

    # nice formattet full output, if anyone need is
    nice_format = {}
    for question in score_results:
        question_scores = nice_format.setdefault(question, [])
        for combination_string in score_results[question]:
            combo = score_results[question][combination_string]
            del combo['scores']
            question_scores.append(combo)

    with open('result/evaluation_only_avg' + '.json', 'w') as data_file:
        data_file.write(json.dumps(nice_format, sort_keys=False, indent=4))
        data_file.close()
