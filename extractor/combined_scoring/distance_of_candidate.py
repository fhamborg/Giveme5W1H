from typing import List

from combined_scoring.abs_combined_scoring import AbsCombinedScoring
from document import Document


class DistanceOfCandidate(AbsCombinedScoring):
    """
    re-score the how dependant_questions-candidates bases on the sentence-distance
    to the best primary_questions-candidates.
    """

    def __init__(self, primary_questions: List[str] = ['what', 'who'], dependant_questions: str = 'how',
                 weight=[1, 1, 1]):
        """

        1.


        :param primary_questions
        :param dependant_questions
        :param weight: (candidates_taken into account, majorQuestions_A, majorQuestions_B).
        First weight indicated how important the distance of candidates in general is. Following weights adjust the influence per major.
        Set to 1 for equal



        """
        self._primary_questions = primary_questions
        self._dependant_questions = dependant_questions
        self._weight = weight

    def score(self, document: Document):
        distance_matrix = {}
        d_candidates = document.get_answer(self._dependant_questions)
        for question in self._primary_questions:
            m_candidates = document.get_answer(question)

            if len(m_candidates) == 0:
                # no candidates to compare with, nothing to to here
                return

            distance_matrix[question] = []

            max = -99
            min = 99

            for i, d_candidate in enumerate(d_candidates):
                # calculate the avg distance to the first n candidates
                d_index = d_candidate.get_sentence_index()
                counter = 0
                _sum = 0
                for m_candidate in m_candidates:
                    if counter >= self._weight[0]:
                        break
                    _sum += abs(m_candidate.get_sentence_index() - d_index)
                    counter += 1
                    avgDist = _sum / counter

                if min > avgDist:
                    min = avgDist
                if max < avgDist:
                    max = avgDist
                distance_matrix[question].append(_sum / counter)
            distance_matrix[question + '_max'] = max
            distance_matrix[question + '_min'] = min

        # normalisation - reversed - small distance ==> sore increases more
        for question in self._primary_questions:
            min = distance_matrix[question + '_min']
            max = distance_matrix[question + '_max']
            max_minus_min = max - min
            for i, dist in enumerate(distance_matrix[question]):
                normDist = (max - dist) / max_minus_min
                distance_matrix[question][i] = normDist

        for i, d_candidate in enumerate(d_candidates):
            dist_factor = 0
            for iq, question in enumerate(self._primary_questions):
                dist_factor += distance_matrix[question][i] * self._weight[iq]
            dist_factor = dist_factor / len(distance_matrix)

            score = d_candidate.get_score() + dist_factor
            d_candidate.set_score(score)

        # resort the candidates
        d_candidates.sort(key=lambda x: x.get_score(), reverse=True)

        # TODO: Normalize afterwards?

        return None
