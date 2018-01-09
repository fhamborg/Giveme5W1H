import json
import csv
from os import listdir
from os.path import isfile, join

"""
Extracts information required (or convenient) for the evaluation.
"""


path_extracted_dataset = '/Users/felix/IdeaProjects/Giveme5W/examples/datasets/bbc/output'
empty_line = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

onlyfiles = [f for f in listdir(path_extracted_dataset) if isfile(join(path_extracted_dataset, f))]


def get_answer(article, question):
    answers = article['fiveWoneH']
    answer = answers[question]['extracted']
    if answer:
        if question == 'when':
            return answer[0]['text'] + ' | ' + answer[0]['enhancement']['timex']['start_date']
        else:
            return answer[0]['text']
    else:
        return ""


csv_writer = csv.writer(open('evaluate.csv', 'w'), delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow(['category', 'who', 'who2', 'what', 'what2', 'when', 'when2', 'where', 'where2', 'why', 'why2', 'how', 'how2', 'open'])

for json_file in onlyfiles:
    if not json_file.endswith('.json'):
        continue

    path_cur_file = join(path_extracted_dataset, json_file)
    print(path_cur_file)

    article = json.load(open(path_cur_file))
    did = article['dId']

    who = get_answer(article, 'who')
    what = get_answer(article, 'what')
    when = get_answer(article, 'when')
    where = get_answer(article, 'where')
    why = get_answer(article, 'why')
    how = get_answer(article, 'how')

    pub_date = article['date_publish']
    #category = article['newsCluster']['Category']
    category = article['category']

    csv_writer.writerow([category, who, '', what, '', when, '', where, '', why, '', how, '', "open " + path_cur_file])
    csv_writer.writerow(empty_line)
