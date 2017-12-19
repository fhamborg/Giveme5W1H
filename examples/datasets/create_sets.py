"""
Helper tp create a sampling.json for each dataset.
Each set has a list of random selected filenames (testing and training 80/20).

"""
import json
import random

import os
from glob import glob


def create_sets(path, testing_size: float=0.8):
    """
    return dataset directories
    :return:
    """
    #glob_pattern = os.path.join(path, '/data/*.json')
    files = glob(path + 'data/*.json')
    random.shuffle(files)

    for i,file in enumerate(files):
        files[i] = os.path.basename(file)

    entire_set_size = len(files)
    absolute_testing_set_size =  int(entire_set_size * testing_size)

    return {
        'training': files[:absolute_testing_set_size],
        'test':  files[absolute_testing_set_size:]
    }

def get_data_sets():
    """
    return dataset directories
    :return:
    """
    return glob(os.path.join('./', '*/'))


if __name__ == '__main__':

    for dataset in get_data_sets():
        sampling = create_sets(dataset)
        with open(dataset + '/sampling.json', 'w', encoding='utf-8') as outfile:
            json_dump = json.dumps(sampling, sort_keys=False, indent=2)
            outfile.write(json_dump)
            outfile.close()

