import logging
from candidate import Candidate
from abc import ABCMeta, abstractmethod
from itertools import product

import nltk
from nltk.corpus import wordnet


class AbsEnhancer:

    def __init__(self, questions):
        self._questions = questions

    @abstractmethod
    def process(self, document):
        return None

    @abstractmethod
    def enhance(self, document):
        return None
