from .abs_extractor import AbsExtractor


class EnvironmentExtractor(AbsExtractor):

    def extract(self, document):
        """
        Parses the given document for locations and time data

        :param document: The document to analyze
        :return: Processed document
        """

        ne_lists = self._extract_candidates(document)
        locations = self._evaluate_locations(document, ne_lists['LOCATION'])
        dates = self._evaluate_dates(document, ne_lists['DATE'], ne_lists['TIME'])

        self.answer(document, 'where', locations)
        self.answer(document, 'when', dates)

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all phrases containing a preposition.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A List of Tuples containing all prepositions
        """

        # first check the results of the NER
        ne_lists = {'LOCATION': [], 'DATE': [], 'TIME': []}

        #percentage of overlap needed for a location-candidate to join a cluster
        accuracy = 0.2

        for i in range(len(document.nerTags)):
            if limit is not None and limit == i:
                break

            for candidate in self._extract_entities(document.nerTags[i], ['LOCATION', 'TIME', 'DATE'], inverted=True):
                if candidate[1] != 'LOCATION':
                    # just save time related data
                    ne_lists[candidate[1]].append((candidate[0], i))
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

    def _evaluate_locations(self, document, clusters, weights=None):
        ranked_candidates = []

        if weights is None:
            scores = [1, 1]
        else:
            scores = weights

        for cluster in clusters:
            # frequency
            scores[0] *= len(cluster[0])/document.length
            # position
            scores[1] *= (document.length - cluster[1])/document.length

            ranked_candidates.append((cluster[0][0], sum(scores)))

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates

    def _evaluate_dates(self, document, date_list, time_list, weights=None):

        ranked_candidates = []

        if weights is None:
            weights = [1, 1]

        last_date = []

        for i in range(len(date_list)):
            date = date_list[i]
            for time in time_list:
                if time[1] < date[1]:
                    ranked_candidates.append((last_date + time[0], (weights[0] * (time[1] / document.length))))
                elif time[1] == date[1]:
                    ranked_candidates.append((date[0] + time[0], (weights[0] * date[1] / document.length) + weights[1]))
                break

            last_date = date[0]

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates



