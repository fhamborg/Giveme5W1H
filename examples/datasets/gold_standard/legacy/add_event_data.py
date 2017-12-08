import glob
from datetime import date

import os

from flask import json

from datasets.gold_standard.legacy.generate_annotations_new import result


def deep_access(x, path):
    """
    elegant deep access to dicts path can be giveme5w.annotated.how.text
    :param x:
    :param path:
    :return:
    """
    key_list = path.split('.')
    val = x
    for key in key_list:
        if val :
            if isinstance(val, list):
                val = val[int(key)]
            else:
                val = val.get(key)
        else:
            return None
    return val



"""
this script adds the exact event date to each annotated when phrase under "parsed".
Adjust them afterwards by hand
"""
event_dates = {
    "f1": date(2017, 11, 13),
    "trump and obama": date(2017, 11, 10),
    "seattle shooting": date(2017, 11, 9),
    "gaga protests": date(2017, 11, 9),
    "cubs win championship": date(2016, 11, 2),
    "china well": date(2016, 11, 12),
    "clinton blames comey": date(2016, 11, 12),
    "clinton clear": date(2017, 11, 7),
    "consulate attack": date(2016, 11, 10),
    "toberone-gate": date(2016, 11, 8),
    "tram": date(2017, 11, 9),
    "tram victims": date(2017, 11, 12)
}

# make it json-able
for event_date in event_dates:
    event_dates[event_date] = event_dates[event_date].isoformat()

for filepath in glob.glob(os.path.dirname(__file__) + '/../data/*.json'):

    with open(filepath, encoding='utf-8') as data_file:
        data = json.load(data_file)

    if data.get('category') is not None:
        annotated = deep_access(data, 'fiveWoneH.when.annotated')
        if annotated is not None:
            for anno in annotated:
                anno['parsed'] = event_dates[data['category']]

        #save it back
        with open(filepath, 'w', encoding='utf8') as outfile:
            outfile.write(json.dumps(data, indent=2, sort_keys=True))
            outfile.close()

print('done')