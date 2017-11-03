import os
import csv
from extractor.tools.file.handler import Handler
import time


# Convert the extracted answers to csv file for further evaluation
# format is: dId,title, category, score, text, Coder-ICR-placeholder-1, Coder-ICR-placeholder-2, Coder-ICR-placeholder-3
# see "Setup:" to run it for the golden_standart annotations


# Coder-ICR-placeholder-x must be set by hand with a scale from 0 to 2
# (0) non-relevant (if an answer contains no relevant information,
# (1) partially relevant (if part of the answer is relevant or information is missing)
# (2) relevant (if the answer is completely relevant without missing information).


# Details on ICR:
# https://www.pcc.edu/resources/academic/learning-assessment/documents/2014_11_21_LACMtg2InterRaterReliability.pdf

# set the question here
questions = [['how','when','why','where','what','who']]
# number of included candidates (obviously, they should be part in the input files)
# set it to one for evaluation per document
candidates = 1


# Setup: evaluation of giveme5W output
## input files: usually the output directory of giveme5w
inputPath = os.path.dirname(__file__) + '/../extracting/output'
accessor = 'extracted'


# Setup: evaluation of ggolden_standard
# input files
inputPath = os.path.dirname(__file__) + '/../extracting/output'
accessor = 'annotated'


# extracting
def get_parts_as_text(parts):
    answer_text = None
    for part in parts:
        if answer_text:
            answer_text = answer_text + ' ' + part[0]['nlpToken'].get('originalText')
        else:
            answer_text = part[0]['nlpToken'].get('originalText')
    return answer_text

# init with initial header line
outputs = {}
for question in questions:
    outputs[question] = [('dId', 'title', 'category', 'score', 'text', 'Coder-ICR-1', 'Coder-ICR-2', 'Coder-ICR-3')]

# Usage of the handler to get the documents
documents = Handler(inputPath).preload_and_cache_documents().get_documents()

for document in documents:
    raw = document.get_rawData()

    for question in questions:
        answers = raw['fiveWoneH'][question]['extracted']
        if answers:
            counter = 0
            for candidate in answers:
                outputs[question].append([str(document.get_document_id()), raw.get('title','noTitle'), raw.get('category','noCategory'), str(candidate['score']), get_parts_as_text(candidate.get('parts')),-1,-1,-1])
                counter = counter + 1
                if counter == candidates:
                    break

# write it back
timestamp =  str(time.time()) # this is preventing the override of files, which may have been annotated by coder already
for question in questions:

    with open(os.path.dirname(__file__) + '/evaluation_data_' + question + '_' + timestamp+ '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in outputs:
            writer.writerow(line)


