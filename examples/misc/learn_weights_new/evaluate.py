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
    #filename = os.path.basename(file_path)
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

if __name__ == '__main__':

    # read all available prickles
    score_results = read_file('queue_caches/*processed.prickle')

    # 1. Crit.: has a high score on average per weight (documents are merged)t
    score_per_average = {}
    for question in score_results:
        for combination_string in score_results[question]:
            combo = score_results[question][combination_string]
            a_sum = sum(combo['scores_doc'])

            combo['avg'] = a_sum / len(combo['scores_doc'])
            score_per_average[combination_string] = {
                'score': a_sum
            }

    # write raw results
    with open('result/evaluation_full'+'.json', 'w') as data_file:
        data_file.write(json.dumps(score_results, sort_keys=False, indent=4))
        data_file.close()


    # has a high score on average per weight (documents are merged)


    # has a high score per document top N weights per document are merged into a list
    best_weight_per_document = {}

    # lowest error rate per weight ( -minus values, ignoring -1 that's no annotation?)
    results_error_rate = {}



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
