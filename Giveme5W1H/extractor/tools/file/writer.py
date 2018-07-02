import json
import pickle

import os

from Giveme5W1H.extractor.candidate import Candidate
from Giveme5W1H.extractor.configuration import Configuration as Config


class Writer:
    """
    Helper to write prickles and json representations of documents
    There is no way to convert a json back to a full document object. Use prickles instead
    """

    def __init__(self):
        """
        :param path: Absolute path to the output directory
        """
        self._preprocessedPath = None

    def _write_json(self, output_object):
        outfile = open(self._outputPath + '/' + output_object['dId'] + '.json', 'w')
        outfile.write(json.dumps(output_object, sort_keys=False, indent=2))
        outfile.close()

    def write_pickle(self, document):
        #deprecated
        with open(self.get_preprocessed_filepath(document.get_rawData()['dId']), 'wb') as f:
            # Pickle the 'data' document using the highest protocol available.
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

    def write_pickle_file(self, path, file):
        fullpath = self._preprocessedPath + '/' + path + '.pickle'
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath , 'wb') as f:
            pickle.dump(file, f, pickle.HIGHEST_PROTOCOL)

    def get_preprocessed_filepath(self, id):
        #deprecated
        return self._preprocessedPath + '/' + id + '.pickle'

    def get_preprocessed_path(self):
        return self._preprocessedPath

    def set_preprocessed_path(self, preprocessed_path):
        self._preprocessedPath = preprocessed_path

    def setOutputPath(self, output_path):
        self._outputPath = output_path

    def generate_json(self, document):

        """
        :param document: The parsed Document
        :type document: Document

        :return: None
        """

        # Reuse the input json as template for the output json
        output = document.get_rawData()

        if output is None:
            output = {}

        # Check if there isn`t already a fiveWoneH literal
        five_w_one_h_literal = output.setdefault('fiveWoneH', {})

        # Save error flags(not under fiveWoneH, would break further code which expects there only questions)
        output.setdefault('fiveWoneH_Metadata', {
            'process_errors': document.get_error_flags()
        })

        if Config.get()['fiveWoneH_enhancer_full']:
            output.setdefault('fiveWoneH_enhancer', document.get_enhancements() )

        # Extract answers
        answers = document.get_answers()

        for question in answers:
            # check if question literal is there
            question_literal = five_w_one_h_literal.setdefault(question, {'extracted': []})

            # add a label, thats only there for the ui
            if Config.get()['label']:
                question_literal['label'] = question

            # check if extracted literal is there
            extracted_literal = question_literal.setdefault('extracted', [])
            for answer in answers[question]:
                if isinstance(answer, Candidate):
                    # answer was already refactored
                    awJson = answer.get_json()
                    # clean up json by skipping NULL entries
                    if awJson:
                        extracted_literal.append(awJson)

                else:
                    # fallback for none refactored extractors
                    candidate_json = {'score': answer[1], 'words': []}
                    for candidateWord in answer[0]:
                        candidate_json['parts'].append({'text': candidateWord[0], 'nlpTag': candidateWord[1]})
                    extracted_literal.append(candidate_json)

                if Config.get()['onlyTopCandidate']:
                    # stop after the first answer
                    break
        return output

    def write(self, document):
        if self._outputPath:
            a_json = self.generate_json(document)
            self._write_json(a_json)
        else:
            print("set a outputPath before writing")
