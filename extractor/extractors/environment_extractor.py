from .abs_extractor import AbsExtractor
from copy import deepcopy
import dateutil.parser as dparser

class EnvironmentExtractor(AbsExtractor):
    weights = ((1, 1), (10, 1, 1, 5))  # ((loc_pos, loc_freq), (time_pos, time_date, time_time, time_dateutil))

    def extract(self, document):
        """
        Parses the given document for locations and time data

        :param document: The document to analyze
        :return: Processed document
        """

        ne_lists = self._extract_candidates(document)
        locations = self._evaluate_locations(document, ne_lists['LOCATION'])
        dates = self._evaluate_dates(document, ne_lists['DATE'], ne_lists['TIME'], ne_lists['TIME+DATE'])

        self.answer(document, 'where', locations)
        self.answer(document, 'when', dates)

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all locations, dates and times.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A dictionary containing all entities sorted by locations, dates, times and time+date
        """

        # first check the results of the NER
        ne_lists = {'LOCATION': [], 'DATE': [], 'TIME': [], 'TIME+DATE': []}

        #percentage of overlap needed for a location-candidate to join a cluster
        accuracy = 0.4

        for i in range(len(document.nerTags)):
            if limit is not None and limit == i:
                break

            for candidate in self._extract_entities(document.nerTags[i], ['LOCATION', 'TIME', 'DATE'], inverted=True,
                                                    phrase_range=4, groups={'TIME': 'TIME+DATE', 'DATE': 'TIME+DATE'}):
                if candidate[1] != 'LOCATION':
                    # just save time related data
                    ne_lists[candidate[1]].append([candidate[0], i])
                else:
                    # cluster locations
                    similarity = 0
                    j = 0
                    while accuracy > similarity and j < len(ne_lists['LOCATION']):
                        location = ne_lists['LOCATION'][j]

                        # compare names in the cluster with the current candidate
                        for name in location[0]:
                            similarity = self.overlap(candidate[0], name)
                            if similarity > accuracy:
                                location[0].append(candidate[0])
                                break

                        j += 1

                    # no similar name could be found, this must be a new entity
                    if similarity == 0:
                        ne_lists['LOCATION'].append([[candidate[0]], i])
        return ne_lists

    def _evaluate_locations(self, document, clusters):
        """
        Calculate a confidence score for extracted location candidates.

        :param document: The parsed document.
        :param clusters: The extracted locations.
        :param weights: Optional weighting used for the evaluation: [cluster_size, position]
        :return: A list of evaluated and ranked candidates
        """

        ranked_candidates = []
        for cluster in clusters:
            scores = list(self.weights[0])
            cluster[0].sort(reverse=True)

            # position
            scores[0] *= document.length - cluster[1]
            # frequency
            scores[1] *= len(cluster[0])

            ranked_candidates.append((cluster[0][0], sum(scores)))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates

    def _evaluate_dates(self, document, date_list, time_list, date_time_list):
        """
        Calculate a confidence score for extracted time candidates.

        :param document: The parsed document.
        :param date_list: List of date candidates.
        :param time_list: List of time candidates.
        :param date_time_list: List of time+date candidates.
        :return: A list of evaluated and ranked candidates
        """

        ranked_candidates = []
        time_candidates = deepcopy(time_list)

        for candidate in date_time_list:
            scores = list(self.weights[1])
            scores[0] *= (document.length - candidate[1])/document.length

            ranked_candidates.append([candidate[0], scores])

        for candidate in date_list:
            scores = list(self.weights[1])
            scores[0] *= (document.length - candidate[1])/document.length

            for i in range(len(time_candidates)):
                if abs(candidate[1] - time_candidates[i][1]) < 2:
                    scores[2] *= 0.8
                    candidate[0].extend(time_candidates[i][0])
                    time_candidates.pop(i)
                    break
            else:
                scores[2] = 0

            ranked_candidates.append([candidate[0], scores])

        for candidate in time_candidates:
            scores = list(self.weights[1])
            scores[0] *= (document.length - candidate[1])/document.length
            scores[1] = 0

            ranked_candidates.append([candidate[0], scores])

        # try to compute a dateutil-object
        for candidate in ranked_candidates:
            try:
                dparser.parse(' '.join(candidate[0]), fuzzy=True)
            except ValueError as e:
                candidate[1][3]=0
            candidate[1] = sum(candidate[1])

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates



