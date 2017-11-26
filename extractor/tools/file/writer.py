import json
import pickle

from extractor.candidate import Candidate
from extractor.configuration import Configuration as Config


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
        with open(self.get_preprocessed_filepath(document.get_rawData()['dId']), 'wb') as f:
            # Pickle the 'data' document using the highest protocol available.
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

    def get_preprocessed_filepath(self, id):
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

        # reuse the input json as template for the output json
        output = document.get_rawData()

        if output is None:
            output = {}

        # check if there isn`t already a fiveWoneH literal
        fiveWoneHLiteral = output.setdefault('fiveWoneH', {})

        # Extract answers
        answers = document.get_answers()

        for question in answers:
            # check if question literal is there
            questionLiteral = fiveWoneHLiteral.setdefault(question, {'extracted': []})

            # add a label, thats only there for the ui
            if Config.get()['label']:
                questionLiteral['label'] = question

            # check if extracted literal is there
            extractedLiteral = questionLiteral.setdefault('extracted', [])
            for answer in answers[question]:
                if isinstance(answer, Candidate):
                    # answer was already refactored
                    awJson = answer.get_json()
                    # clean up json by skipping NULL entries
                    if awJson:
                        extractedLiteral.append(awJson)

                else:
                    # fallback for none refactored extractors
                    candidate_json = {'score': answer[1], 'words': []}
                    for candidateWord in answer[0]:
                        candidate_json['parts'].append({'text': candidateWord[0], 'nlpTag': candidateWord[1]})
                    extractedLiteral.append(candidate_json)

                if Config.get()['onlyTopCandidate']:
                    # stop after the first not answer
                    break
        return output

    def write(self, document):
        if self._outputPath:
            self._write_json(self.generate_json(document))
        else:
            print("set a outputPath before printing")
