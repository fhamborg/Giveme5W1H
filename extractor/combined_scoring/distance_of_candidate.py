from typing import List

from combined_scoring.abs_combined_scoring import AbsCombinedScoring
from document import Document


class DistanceOfCandidate(AbsCombinedScoring):
    """
    Rescoring of dependant_questions-candidates bases on the sentence-distance to the best primary_questions-candidate(s).

    For two primary_questions a and b; n_top_candidates=1,
    where ABS return the normalized absolute distance between 0..1

    new_score = old_score +
                1-ABS(primary_top_candidate_a_index - dependant_candidate_index) * W1 +
                1-ABS(primary_top_candidate_b_index - dependant_candidate_index) * W2

    For two primary_questions a and b; n_top_candidates=2, this is roughly:
    new_score = old_score +
                AVG(
                      1-ABS(primary_top_candidate_a_index - dependant_candidate_index)
                    + 1-ABS(primary_top-1_candidate_a_index - dependant_candidate_index) ) * W1 +
                AVG(
                    1-ABS(primary_top-1_candidate_b_index - dependant_candidate_index) * W2,
                    1-ABS(primary_top_candidate_b_index - dependant_candidate_index)) * W2)


    Score is Normalized afterwards to 1..0


    """

    def __init__(self, primary_questions: List[str] = ['what'], dependant_questions: str = 'how',
                 n_top_candidates: int = 1,
                 weight=[0.3], normalize: bool = True):
        """
        :param primary_questions
        :param dependant_questions
        :param n_top_candidates: n-top-candidates taken into account from each primary question.
                Distance between is averaged,
        :param weight: primary_questions_weight_a, primary_questions_weight_b ..). Should sum up to 1.
                If 1 primary_questions is used the default & weight has no influence
        """
        self._primary_questions = primary_questions
        self._dependant_questions = dependant_questions
        self._weight = weight
        self._n_top_candidates = n_top_candidates
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

            top_max = float('-inf')
            top_min = float('inf')

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
                if max_minus_min:
                    norm_dist = (top_question_max - dist) / max_minus_min
                else:
                    norm_dist = (top_question_max - dist)
                distance_matrix[question][i] = norm_dist

        candidate_min = float('inf')
        candidate_max = float('-inf')
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
                if max_minus_min:
                    norm_score = (score - candidate_min) / max_minus_min
                else:
                    norm_score = (score - candidate_min)
                d_candidate.set_score(norm_score)

        # resort the candidates
        dependant_candidates.sort(key=lambda x: x.get_score(), reverse=True)

        return None
