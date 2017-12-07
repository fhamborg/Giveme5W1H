from typing import List

from combined_scoring.abs_combined_scoring import AbsCombinedScoring
from document import Document


class DistanceOfCandidate(AbsCombinedScoring):
    """
    re-score the  dependant_questions-candidates bases on the sentence-distance to the best primary_questions-candidates.
    """
    def __init__(self, primary_questions: List[str] = ['what', 'who'], dependant_questions: str = 'how', n_top_candidates: int=1,
                 weight=[1, 1, 1], normalize: bool=True):
        """
        :param primary_questions
        :param dependant_questions
        :param n_top_candidates: n-top-candidates taken into account from each primary question.
                Distance between is averaged,
        :param weight: primary_questions_weight_a, primary_questions_weight_b ..). Should sum up to 1
        """
        self._primary_questions = primary_questions
        self._dependant_questions = dependant_questions
        self._weight = weight
        self._n_top_candidates = 1
        self._normalize = normalize

    def score(self, document: Document):
        distance_matrix = {}
        dependant_candidates = document.get_answer(self._dependant_questions)
        for question in self._primary_questions:
            m_candidates = document.get_answer(question)

            if len(m_candidates) == 0:
                # no candidates to compare with, nothing to to here
                return

            distance_matrix[question] = []

            top_max = -99
            top_min = 99
            for i, d_candidate in enumerate(dependant_candidates):
                # calculate the avg distance to the first n candidates
                d_index = d_candidate.get_sentence_index()
                counter = 0
                _sum = 0
                for m_candidate in m_candidates:
                    if counter >= self._n_top_candidates:
                        break
                    _sum += abs(m_candidate.get_sentence_index() - d_index)
                    counter += 1

                avg_dist = _sum / counter
                top_min = min(avg_dist, top_min)
                top_max = max(avg_dist, top_max)

                distance_matrix[question].append(_sum / counter)
            distance_matrix[question + '_max'] = top_max
            distance_matrix[question + '_min'] = top_min

        # normalisation - reversed - small distance ==> score increases more
        for question in self._primary_questions:
            top_question_min = distance_matrix[question + '_min']
            top_question_max = distance_matrix[question + '_max']
            max_minus_min = top_question_max - top_question_min
            for i, dist in enumerate(distance_matrix[question]):
                norm_dist = (top_question_max - dist) / max_minus_min
                distance_matrix[question][i] = norm_dist

        candidate_min = 99
        candidate_max = -99
        for i, d_candidate in enumerate(dependant_candidates):
            dist_factor = 0
            for iq, question in enumerate(self._primary_questions):
                dist_factor += distance_matrix[question][i] * self._weight[iq]
            dist_factor = dist_factor / len(distance_matrix)

            score = d_candidate.get_score() + dist_factor
            candidate_min = min(candidate_min, score)
            candidate_max = max(candidate_max, score)
            d_candidate.set_score(score)

        if self._normalize is True:
            max_minus_min = candidate_max - candidate_min
            for d_candidate in dependant_candidates:
                score = d_candidate.get_score()
                norm_score = (score - candidate_min) / max_minus_min
                d_candidate.set_score(norm_score)

        # resort the candidates
        dependant_candidates.sort(key=lambda x: x.get_score(), reverse=True)

        return None
