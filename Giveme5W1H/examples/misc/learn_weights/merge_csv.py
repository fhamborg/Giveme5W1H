import csv
from typing import List

def weights_to_string(weights):
    """
    converts an array of ints to a string.
    :param weights:
    :return:
    """
    scaled_weights_string = [str(x) for x in weights]
    return '_'.join(scaled_weights_string)

def load_csv(path, weight_count, score_label = 'score'):
    """
    score row must be labeled with score.

    :param path:
    :return:
    """

    csv_content = []
    header = True
    with open(path + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        # read header

        # read file
        for row in reader:
            if header:
                header = False
                score_index = row.index(score_label)
            else:

                for weight_index in range(0, weight_count):
                    row[weight_index] =  round( float(row[weight_index]), 1) # float fix

                csv_content.append(row)
    csv_content.sort(key=lambda x: x[score_index])

    return csv_content, score_index


def load_weights_and_merge(directory: str, type,  question: str, weight_count: int ):


    path_master = directory + 'test_final_result_' + question + '_1_' + type
    path_slave = directory + 'training_final_result_' + question + '_1_' + type
    path_output = 'result/merges/' + question + '_' + type


    master_csv, master_score_index = load_csv(path_master,weight_count)
    slave_csv, slave_score_index = load_csv(path_slave, weight_count)

    master_merge_csv = {}

    # convert master to object for merge, weights are keys
    for master_csv_line in master_csv:
        weights = master_csv_line[0:weight_count]

        # float to string for scores
        master_csv_line[master_score_index] = float(master_csv_line[master_score_index])
        weights_str = weights_to_string(weights)
        master_merge_csv[weights_str] = master_csv_line

    # loop over loop lave and add scores if match
    for slave_csv_line in slave_csv:

        # float to string for scores
        slave_csv_line[slave_score_index] = float(slave_csv_line[slave_score_index])

        weights = slave_csv_line[0:weight_count]
        weights_str = weights_to_string(weights)
        combo = master_merge_csv.get(weights_str)
        if combo:
            # merge
            score_slave = slave_csv_line[slave_score_index]
            combo.append(score_slave)


    master_merge_list = list(master_merge_csv.values())

    with open(path_output + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in master_merge_list:
            writer.writerow(line)

if __name__ == '__main__':

    # default

   # ty = 'avg' # 'avg'

    for ty in ['avg','norm_score']:

        weight_count = 4
        for question in ['how','why', 'where']:
            load_weights_and_merge( question=question,
                                    type=ty,
                                    directory='result/wmd/default/',
                                    weight_count=weight_count
                                    )
        weight_count = 3
        for question in ['what', 'who']:
            load_weights_and_merge(question=question,
                                   type=ty,
                                   directory='result/wmd/default/',
                                   weight_count=weight_count
                               )

        weight_count = 5
        for question in ['when']:
            load_weights_and_merge(question=question,
                                   type=ty,
                                   directory='result/wmd/wmd_when_fix_entailment/',
                                   weight_count=weight_count
                                   )