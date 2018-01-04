import spacy
import wmd as wm
import logging
import math


from misc.learn_weights_new.metrics.abs_metric import AbsMetric


class Wmd(AbsMetric):
    """
    https://github.com/src-d/wmd-relax
    paper: http://www.cs.cornell.edu/~kilian/papers/wmd_metric.pdf

    install: https://github.com/google/or-tools

    """
    def __init__(self, *args, **kwargs):
        super(Wmd, self).__init__(*args, **kwargs)
        # nlp = spacy.load('en', create_pipeline=wm.WMD.create_spacy_pipeline)
        self._nlp = spacy.load('en_vectors_web_lg')


    def calculate_distance(self, candidates_a, candidates_b):
        """
        :param candidates_a:
        :param candidates_b:
        :return:
        """

        # special case two None, so this articles had no answer -> similar -> low distance
        if candidates_a is None and candidates_b is None:
            result = 0
        elif candidates_a == candidates_b:
            result = 0
        else:
            cache_content = self._cache.get_complex([candidates_a, candidates_b])
            if cache_content:
                result = cache_content
                # print('cached hit')
            else:
                doc1 = self._nlp(candidates_a)
                doc2 = self._nlp(candidates_b)
                result = (doc1.similarity(doc2))
                # flip from Similarity to Distance
                result = 1 - result

                # under some rare conditions result is nearby, but below 0 or 1
                # this leads to wrong evaluation results because negative values are used for errors
                if result < 0:
                    result = 0
                if result > 1:
                    result = 1

                self._cache.cache_complex([candidates_a, candidates_b], result)
                # print('cached')
        # print([candidates_a, candidates_b], end=" ")
        # print(result)
        return result
