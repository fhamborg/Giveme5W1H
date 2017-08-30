class DistanceOfCandidate:
    # re-score the how candidates bases on the proximity to the Who and What candidates
    # documentObject, ['who','what'], 'How', weight=[1] (number of major candidates for dist calculation, weightMajorA, weightMajorB... )
    def __init__(self, majorQuestions, dependantQuestions, weight=[3, 1, 1]):
        self._majorQuestions = majorQuestions
        self._dependantQuestions = dependantQuestions
        self._weight = weight

    # documentObject, ['Who','What'], ['How'], weight=1
    def score(self, document):

        distanceMatrix = {}

        d_candidates = document.get_answer(self._dependantQuestions)
        for question in self._majorQuestions:
            m_candidates = document.get_answer(question)

            if len(m_candidates) == 0:
                # no candidates to compare with, nothing to to here
                return

            distanceMatrix[question] = []
            max = -99
            min = 99
            for i, d_candidate in enumerate(d_candidates):
                # callculate the avg distance to the firs n candidates
                d_index = d_candidate.get_sentence_index()
                counter = 0
                sum = 0
                for m_candidate in m_candidates:
                    if counter >= self._weight[0]:
                        break
                    #
                    sum += abs(m_candidate.get_sentence_index() - d_index)
                    counter += 1

                    avgDist = sum / counter

                if min > avgDist:
                    min = avgDist
                if max < avgDist:
                    max = avgDist
                distanceMatrix[question].append(sum / counter)
            distanceMatrix[question + '_max'] = max
            distanceMatrix[question + '_min'] = min

        # print(distanceMatrix)
        # normalisation - reversed small distance ==> sore increases more
        for question in self._majorQuestions:
            min = distanceMatrix[question + '_min']
            max = distanceMatrix[question + '_max']
            maxMinusMin = max - min
            for i, dist in enumerate(distanceMatrix[question]):
                normDist = (max - dist) / maxMinusMin
                distanceMatrix[question][i] = normDist

        for i, d_candidate in enumerate(d_candidates):

            distFactor = 0
            for iq, question in enumerate(self._majorQuestions):
                distFactor += distanceMatrix[question][i] * self._weight[iq]
            distFactor = distFactor / len(distanceMatrix)

            score = d_candidate.get_score() + distFactor
            d_candidate.set_score(score)

        # resort the candidates
        d_candidates.sort(key=lambda x: x.get_score(), reverse=True)

        return None
