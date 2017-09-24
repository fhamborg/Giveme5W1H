import hashlib
import json
import logging
import os.path
import pickle

from document import Document


class Reader(object):
    def __init__(self):
        # self.factory = DocumentFactory()
        self.log = logging.getLogger('GiveMe5W')
        self._preprocessedPath = None

    def set_preprocessed_path(self, preprocessed_path):
        self._preprocessedPath = preprocessed_path
        return self

    def get_preprocessed_path(self):
        return self._preprocessedPath

    def get_preprocessed_filepath(self, id):
        return self._preprocessedPath + '/' + id + '.pickle'

    def read(self, path):
        with open(path, encoding='utf-8') as data_file:
            data = json.load(data_file)
            url = data.setdefault('url', None)
            if not url:
                print(path + ' has not URL. A URL is mandatory to generate a unique document id')

            # generate an (document)id, That the best way to get a unique name.

            data['dId'] = hashlib.sha224(data['url'].encode('utf-8')).hexdigest()

            # path where the preprocessed file should be

            preprocessedFilePath = None
            if self._preprocessedPath is not None:
                preprocessedFilePath = self.get_preprocessed_filepath(data['dId'])

            # preprocessed path and file and file is not empty
            if preprocessedFilePath and os.path.isfile(preprocessedFilePath) and os.path.getsize(preprocessedFilePath) > 0:
                # _preprocessedPath path is given, and there is already a preprocessed document
                with open(preprocessedFilePath, 'rb') as ff:
                    document = pickle.load(ff)
            else:
                document = Document(data.setdefault('title', ''), data.setdefault('description', ''),
                                    data.setdefault('text', ''), data)

                url = data.setdefault('url', None)
                if not url:
                    print(path + ' has not URL. A URL is mandatory to generate a unique document id')
                else:
                    document.set_source(data['url'])

                # load annotations if any
                if 'fiveWoneH' in data:
                    annotationsForGivMe5W = {}
                    # load the questions
                    for question in data['fiveWoneH']:
                        # check if there is a annotatedLiteral
                        if 'annotated' in data['fiveWoneH'][question]:
                            annotated = data['fiveWoneH'][question]['annotated']
                            # check if the literal holds data
                            if annotated is not None:
                                tmp_anno = annotationsForGivMe5W.setdefault(question, [])
                                for annotation in annotated:
                                    # None, None is added for comp. reasons
                                    tmp_anno.append([None, None, annotation['text']])
                    document.set_annotations(annotationsForGivMe5W)

        return document
