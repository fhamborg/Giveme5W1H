from .abs_extractor import AbsExtractor
from copy import deepcopy
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import dateutil.parser as dparser

class EnvironmentExtractor(AbsExtractor):
    weights = ((1, 1), (10, 1, 1, 5))  # ((loc_pos, loc_freq), (time_pos, time_date, time_time, time_dateutil))

    def extract(self, document):
        """
        Parses the given document for locations and time data

        :param document: The document to analyze
        :return: Processed document
        """
        geo_domain = 'nominatim.openstreetmap.org'
        self.geocoder = Nominatim(domain=geo_domain, timeout=2)

        ne_lists = self._extract_candidates(document)
        locations = self._evaluate_locations(document, ne_lists['LOCATION'])
        dates = self._evaluate_dates(document, ne_lists['DATE'], ne_lists['TIME'], ne_lists['TIME+DATE'])

        document.set_answer('where', locations)
        document.set_answer('when', dates)

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all locations, dates and times.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A dictionary containing all entities sorted by locations, dates, times and time+date
        """

        # first check the results of the NER
        ner_tags = document.get_ner()
        ne_lists = {'LOCATION': [], 'DATE': [], 'TIME': [], 'TIME+DATE': []}

        for i in range(len(ner_tags)):
            if limit is not None and limit == i:
                break

            for candidate in self._extract_entities(ner_tags[i], ['LOCATION', 'TIME', 'DATE'], inverted=True,
                                                    phrase_range=2, groups={'TIME': 'TIME+DATE', 'DATE': 'TIME+DATE'}):
                if candidate[1] != 'LOCATION':
                    # just save time related data
                    ne_lists[candidate[1]].append([candidate[0], i])
                else:
                    # geocode retrieved entities
                    location = self.geocoder.geocode(' '.join(candidate[0]))
                    if location is not None:
                        ne_lists['LOCATION'].append((candidate[0], location, i))

        return ne_lists

    def _evaluate_locations(self, document, candidates):
        """
        Calculate a confidence score for extracted location candidates.

        :param document: The parsed document.
        :param candidates: List of tuples containing the extracted candidates: (tokens, geocode, position)
        :return: A list of evaluated and ranked candidates
        """
        raw_locations = []
        unique_locations = []
        ranked_locations = []

        for location in candidates:
            bb = location[1].raw['boundingbox']  # bb contains min lat, max lat, min long, max long
            area = int(vincenty((bb[0], bb[2]), (bb[0], bb[3])).meters) \
                * int(vincenty((bb[0], bb[2]), (bb[1], bb[2])).meters)
            for i in range(4):
                bb[i] = float(bb[i])
            raw_locations.append([location[0], location[1].raw['place_id'],
                                  location[1].point, bb, area, location[2], 0])

        # sort locations based id
        raw_locations.sort(key=lambda x: x[1], reverse=True)

        # count multiple mentions
        for i in range(len(raw_locations)):
            location = raw_locations[i]
            positions = [raw_locations[i][5]]

            for alt in raw_locations[i+1:]:
                if location[1] == alt[1]:
                    positions.append(alt[5])

            location[5] = min(positions)
            location[6] = len(positions)
            unique_locations.append(location)
            i += len(positions)-1

        # sort locations based on size/area
        unique_locations.sort(key=lambda x: x[4], reverse=True)

        # check entailment
        for i in range(len(unique_locations)):
            location = unique_locations[i]
            for alt in raw_locations[i + 1:]:
                if alt[3][0] >= location[2][0] >= alt[3][1] and alt[3][2] >= location[2][1] >= alt[3][3]:
                    # add parent's number of mentions
                    location[6] += alt[6]

            score = self.weights[0][0] * (document.get_len() - location[5]) + self.weights[0][1] * location[6]
            ranked_locations.append((location[0], score))

        ranked_locations.sort(key=lambda x: x[1], reverse=True)
        return ranked_locations

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
        weights = self.weights[1]

        for candidate in date_time_list:
            scores = [0] * len(weights)
            scores[0] = weights[0] * (document.get_len() - candidate[1])/document.get_len()
            scores[1] = weights[1]
            scores[2] = weights[2]

            ranked_candidates.append([candidate[0], deepcopy(scores)])

        for candidate in date_list:
            scores = [0] * len(weights)
            scores[0] = weights[0] * (document.get_len() - candidate[1]) / document.get_len()
            scores[1] = weights[1]

            for i in range(len(time_candidates)):
                # look for time-data in adjacent sentences
                if abs(candidate[1] - time_candidates[i][1]) < 2:
                    scores[2] = weights[2] * 0.8
                    candidate[0].extend(time_candidates[i][0])
                    time_candidates.pop(i)
                    break

            ranked_candidates.append([candidate[0], deepcopy(scores)])

        for candidate in time_candidates:
            scores = [0] * len(weights)
            scores[0] = weights[0] * (document.get_len() - candidate[1]) / document.get_len()
            scores[2] = weights[2]

            ranked_candidates.append([candidate[0], deepcopy(scores)])

        # try to compute a dateutil-object
        for candidate in ranked_candidates:
            try:
                dparser.parse(' '.join(candidate[0]), fuzzy=True)
            except ValueError as e:
                candidate[1][3] = 0
            candidate[1] = sum(candidate[1])

        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates



