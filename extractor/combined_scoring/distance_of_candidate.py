class DistanceOfCandidate:
    # re-score the how candidates bases on the proximity to the Who and What candidates
    # documentObject, ['who','what'], 'How', weight=1
    def __init__(self, majorQuestions, dependantQuestions, weight=1):
        self._majorQuestions = majorQuestions
        self._dependantQuestions = dependantQuestions
        self._weight = weight

    # documentObject, ['Who','What'], ['How'], weight=1
    def score(self, document):
        # dependantAnswers = document.get_answers()[self._dependantQuestions]
        # distances = []

        # for majorQuestion in self._majorQuestions:
        # get the best answer for a major
        #    answer = document.get_answers()[majorQuestion][0]

        # calculate the distance to each dependantAnswers
        #     distances[majorQuestion] = []
        #     for dependantAnswer, index in dependantAnswers:
        #         distances[majorQuestion][index] = answer[3] - dependantAnswer[3]

        # adjust scoring
        # TODO normalise index
        # candidate['positionNorm'] = (self._maxIndex -  candidate['position']) / self._maxIndex

        return None
