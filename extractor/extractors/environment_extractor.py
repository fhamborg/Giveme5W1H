import time
from .abs_extractor import AbsExtractor
from copy import deepcopy
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from parsedatetime import parsedatetime as pdt
import dateutil.parser as dparser


class EnvironmentExtractor(AbsExtractor):
    weights = ((1, 1), (2, 2, 1, 1))  # ((loc_pos, loc_freq), (time_pos, time_date, time_time, time_neigbours))

    def __init__(self, weights=None, overwrite=True):
        """
        :param overwrite: determines if existing answers should be overwritten.
        """
        if weights is not None:
            self.weights = weights

        self.overwrite = overwrite
        geo_domain = 'nominatim.openstreetmap.org'
        self.geocoder = Nominatim(domain=geo_domain, timeout=2)
        self.calendar = pdt.Calendar()
        self.time_dela = 129600  # 32h in seconds

    def extract(self, document):
        """
        Parses the given document for locations and time data

        :param document: The document to analyze
        :return: Processed document
        """

        ne_lists = self._extract_candidates(document)
        locations = self._evaluate_locations(document, ne_lists[0])
        dates = self._evaluate_dates(document, ne_lists[1])

        document.set_answer('where', self._filter_duplicates(locations, False))
        document.set_answer('when', self._filter_duplicates(dates, False))

    def _extract_candidates(self, document, limit=None):
        """
        Extracts all locations, dates and times.

        :param document: The Document to be analyzed.
        :param limit: Number of sentences that should be analyzed.
        :return: A dictionary containing all entities sorted by locations, dates, times and time+date
        """

        # first check the results of the NER
        ner_tags = document.get_ner()
        locations = []
        dates = []
        last_date = None

        for i in range(len(ner_tags)):
            if limit is not None and limit == i:
                break
            for candidate in self._extract_entities(ner_tags[i], ['LOCATION', 'TIME', 'DATE'], inverted=True,
                                                    phrase_range=2, groups={'TIME': 'TIME+DATE', 'DATE': 'TIME+DATE'}):

                if candidate[1] == 'LOCATION':
                    # geocode retrieved entities
                    location = self.geocoder.geocode(' '.join(candidate[0]))
                    if location is not None:
                        locations.append((candidate[0], location, i))
                elif candidate[1] == 'TIME':
                    # try to associate a date to the given time
                    if last_date is not None:
                        dates.append((last_date + candidate[0],i))
                    else:
                        dates.append((last_date + candidate[0], i))
                else:
                    # save date and update last_date
                    dates.append([candidate[0], i])
                    last_date = candidate[0]

        return locations, dates

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
        weights = self.weights[0]
        weights_sum = sum(weights)

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
        max_n = 0
        for index, location in enumerate(unique_locations):
            for alt in raw_locations[index + 1:]:
                if alt[3][0] >= location[2][0] >= alt[3][1] and alt[3][2] >= location[2][1] >= alt[3][3]:
                    # add parent's number of mentions
                    location[6] += alt[6]
            max_n = max(max_n, location[6])

        for location in unique_locations:
            score = weights[0] * (document.get_len() - location[5])/document.get_len() + weights[1] * location[6]/max_n
            if score > 0:
                score /= weights_sum
            ranked_locations.append((location[0], score))

        ranked_locations.sort(key=lambda x: x[1], reverse=True)
        return ranked_locations

    def _evaluate_dates(self, document, date_list):
        """
        Calculate a confidence score for extracted time candidates.

        :param document: The parsed document.
        :param date_list: List of date candidates.
        :param time_list: List of time candidates.
        :param date_time_list: List of time+date candidates.
        :return: A list of evaluated and ranked candidates
        """

        ranked_candidates = []
        weights = self.weights[1]
        weights_sum = sum(weights)
        reference = self.calendar.parse(document.get_date() or '')

        for candidate in date_list:
            date_str = ' '.join(candidate[0])
            if date_str.lower().strip() == 'now':
                continue
            parse = self.calendar.parse(date_str, reference[0])
            if parse[1] > 0:
                # date could be parsed
                ranked_candidates.append([candidate[0], candidate[1], parse[0], parse[1], 1])

        ranked_candidates.sort(key=lambda x: x[2])

        # count 'neighbours' within time_delta range
        max_n = 0
        for index, candidate in enumerate(ranked_candidates):
            for neighbour in ranked_candidates[index+1:]:
                if (time.mktime(neighbour[2]) - time.mktime(candidate[2])) <= self.time_dela:
                    candidate[4] += 1
                    neighbour[4] += 1
            max_n = max(max_n, candidate[4])

        # calculate the scores
        for candidate in ranked_candidates:
            score = weights[0] * (document.get_len() - candidate[1])/document.get_len()     # position
            if candidate[3] == 1:
                score += weights[1]                 # date
            elif candidate[3] == 2:
                score += weights[2]                 # time
            else:
                score += weights[1] + weights[2]    # date + time
            score += weights[3] * (candidate[4]/max_n)  # neighbourhood/frequency

            if score > 0:
                score /= weights_sum
            candidate[1] = score

        ranked_candidates = [(c[0], c[1]) for c in ranked_candidates]
        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates



