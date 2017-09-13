import logging
from candidate import Candidate
from abc import ABCMeta, abstractmethod
from itertools import product

import nltk
from nltk.corpus import wordnet


target = {"part": "part"
           "candidate" "candidate"}


class AbsEnhancer:

    def __init__(self, questions, tar= target.part):
        self._questions = questions
        self._target = tar

    @abstractmethod
    def process(self, document):
        return None

    @abstractmethod
    def enhance(self, document):
        return None
