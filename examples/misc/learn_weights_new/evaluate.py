"""
checks all result files an writes the best candidates to evaluate.json
"""
import glob
import json
import pickle

import statistics

def weights_to_string(weights):
    scaled_weights_string = [str(x) for x in weights]
    return ''.join(scaled_weights_string)

def stats(numbers):
    return {"mean": statistics.mean(numbers),
            "median": statistics.median(numbers)}

def read_file(results, file_path, score_results):
    #filename = os.path.basename(file_path)
    for result in results:
        for question in result:
            question_scores = score_results.setdefault(question, {})
            weights = result[question][1]

            comb = question_scores.setdefault(weights_to_string(weights), {'weights': weights, 'scores': []})
            if result[question][2] != -1:
                print('a')
            comb['scores'].append(result[question][2])

if __name__ == '__main__':

    score_results = {}
    for file_path in glob.glob('queue_caches/*processed.prickle'):
        with open(file_path, 'rb') as ff:
            results = pickle.load(ff)
        read_file(results, file_path, score_results)

    for question in score_results:
        for combination_string in score_results[question]:
            combo = score_results[question][combination_string]
            a_sum = sum(combo['scores'])

            combo['avg'] = a_sum / len(combo['scores'])

    with open('result/evaluation_full'+'.json', 'w') as data_file:
        data_file.write(json.dumps(score_results, sort_keys=False, indent=4))
        data_file.close()

    nice_format = {}
    for question in score_results:
        question_scores = nice_format.setdefault(question,[])
        for combination_string in score_results[question]:
            combo = score_results[question][combination_string]
            del combo['scores']
            question_scores.append(combo)


    with open('result/evaluation_only_avg'+'.json', 'w') as data_file:
        data_file.write(json.dumps(nice_format, sort_keys=False, indent=4))
        data_file.close()

    # find the best weights per document (per question)

    # find the best weights per average score (per question)


