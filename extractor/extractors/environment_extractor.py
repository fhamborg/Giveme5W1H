import copy
import time
import logging
from warnings import catch_warnings

from geopy.distance import great_circle
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim
from parsedatetime import parsedatetime as pdt

from candidate import Candidate
from .abs_extractor import AbsExtractor


class EnvironmentExtractor(AbsExtractor):
    """
    The EnvironmentExtractor tries to extract the location and time the event happened.
    """

    # weights used in the candidate evaluation:
    # ((position, frequency), (position, date, time, frequency))
    weights = ((0.5, 0.8), (0.8, 0.25, 0.2, 0.7))

    def __init__(self, weights=None, host=None):
        """
        Init the Nominatim connection as well as the calender object used for date interpretation.

        :param weights: Weights used to evaluate answer candidates.
        :type weights: ((Float, Float), (Float, Float, Float, Float))
        :param host: Address to the Nominatim host
        :type host: String
        """
        if weights is not None:
            self.weights = weights

        # init db connection used for location resolution
        if host is None:
            host = 'nominatim.openstreetmap.org'

        self.geocoder = Nominatim(domain=host, timeout=8)

        # init calender object for date resolution
        self.calendar = pdt.Calendar()

        # date strings like 'monday' can denote dates in the future as well as in the past
        # in most cases an article describes an event in the past
        self.calendar.ptc.DOWParseStyle = -1  # prefer day in the past for 'monday'
        self.calendar.ptc.CurrentDOWParseStyle = True  # prefer reference date if its the same weekday
        self.time_dela = 86400  # 24h in seconds

    def extract(self, document):
        """
        Parses the given document for locations and time data

        :param document: The Document object to parse
        :type document: Document

        :return: The parsed Document object
        """
        self._extract_candidates(document)
        self._evaluate_candidates(document)

        return document

    def _evaluate_candidates(self, document):

        locations = self._evaluate_locations(document)
        dates = self._evaluate_dates(document)


        document.set_answer('where', locations) # there are now duplicates
        document.set_answer('when', dates)


    def _extract_candidates(self, document):
        """
        Extracts all locations, dates and times.

        :param document: The Document object to parse
        :type document: Document

        :return: A Tuple containing a list of locations and a list of dates.
        """

        # fetch results of the NER
        ner_tags = document.get_ner()
        pos_tags = document.get_pos()
        locations = []
        dates = []
        last_date = None

        tokens = document.get_tokens()

        for i, entity in enumerate(tokens):
            # phrase_range=2 allows entities to be separate by single tokens, this is common for locations and dates
            # i.e. 'London, England' or 'October 13, 2015'.
            for candidate in self._extract_entities(entity, ['LOCATION'], inverted=True, phrase_range=3, accessor='ner'):

                # look-up geocode in Nominatim
                try:
                    location_string = [t['originalText'] for t in candidate[0]]
                    location = self.geocoder.geocode(' '.join(location_string))
                    if location is not None:
                        # fetch pos and append to candidates
                        ca = Candidate()

                        # candidate_object.set_text_index(None)
                        #ca.set_raw((self._fetch_pos(pos_tags[i], candidate[0]), location, i))
                        ca.set_raw(candidate[0])
                        ca.set_sentence_index(i)
                        # thats for the internal evaluation
                        ca.set_calculations('openstreetmap_nominatim', location)
                        # thats for the output
                        ca.set_enhancement('openstreetmap_nominatim', location.raw)


                        locations.append(ca)
                except GeocoderServiceError as e:
                    logging.getLogger('GiveMe5W').error('openstreetmap_nominatim: Where was not extracted ')
                    logging.getLogger('GiveMe5W').error(str(e))
                    # locations.append((self._fetch_pos(pos_tags[i], candidate[0]), location, i))

            for candidate in self._extract_entities(entity, ['TIME', 'DATE'], inverted=True,
                                                    phrase_range=1, groups={'TIME': 'TIME+DATE', 'DATE': 'TIME+DATE'}, accessor='ner'):

                if candidate[1] == 'TIME':
                    # If a date was already mentioned combine it with the mentioned time
                    if last_date is not None:
                        ca = Candidate()

                        # candidate_object.set_text_index(None)
                        #ca.set_raw((last_date + self._fetch_pos(pos_tags[i], candidate[0]), i))
                        ca.set_raw(candidate[0])
                        ca.set_sentence_index(i)
                        dates.append(ca)
                        # dates.append((last_date + self._fetch_pos(pos_tags[i], candidate[0]), i))
                    else:
                        ca = Candidate()

                        # candidate_object.set_text_index(None)
                        #ca.set_raw((self._fetch_pos(pos_tags[i], candidate[0]), i))
                        ca.set_raw(candidate[0])
                        ca.set_sentence_index(i)
                        dates.append(ca)
                        # dates.append((self._fetch_pos(pos_tags[i], candidate[0]), i))
                elif candidate[1] == 'DATE':
                    # dates.append((self._fetch_pos(pos_tags[i], candidate[0]), i))
                    ca = Candidate()

                    # candidate_object.set_text_index(None)
                    #ca.set_raw((self._fetch_pos(pos_tags[i], candidate[0]), i))
                    #dates.append(ca)
                    #ca = self._create_candidate(i, 'pos', tokens, candidate[0])
                    ca.set_raw(candidate[0])
                    ca.set_sentence_index(i)
                    dates.append(ca)
                    last_date = self._fetch_pos(pos_tags[i], candidate[0])
                else:
                    # String includes date and time
                    ca = Candidate()

                    # candidate_object.set_text_index(None)
                    #ca.set_raw((self._fetch_pos(pos_tags[i], candidate[0]), i))
                    #ca = self._create_candidate(i,'pos', tokens,  candidate[0])
                    ca.set_raw(candidate[0])
                    ca.set_sentence_index(i)
                    dates.append(ca)

        document.set_candidates('EnvironmentExtractorNeDates', dates)
        document.set_candidates('EnvironmentExtractorNeLocatios', locations)
        # return locations, dates


    def _evaluate_locations(self, document):
        """
        Calculate a confidence score for extracted location candidates.

        :param document: The parsed document.
        :type document: Document
        :param candidates: List of tuples containing the extracted candidates
        :type candidates: [tokens, geocode, position]

        :return: A list of evaluated and ranked candidates
        """
        raw_locations = []
        unique_locations = []
        ranked_locations = []
        weights = self.weights[0]
        weights_sum = sum(weights)

        for candidate in document.get_candidates('EnvironmentExtractorNeLocatios'):
            # fetch the boundingbox: (min lat, max lat, min long, max long)

            #location = candidate.get_raw()
            #bb = location[1].raw['boundingbox']
            parts = candidate.get_raw()
            location = candidate.get_calculations('openstreetmap_nominatim')
            bb = location.raw['boundingbox']


            # use the vincenty algorithm to calculate the covered area
            area = int(great_circle((bb[0], bb[2]), (bb[0], bb[3])).meters) * int(great_circle((bb[0], bb[2]), (bb[1], bb[2])).meters)
            for i in range(4):
                bb[i] = float(bb[i])
            raw_locations.append([parts, location.raw['place_id'], location.point, bb, area, 0, 0, candidate])

        # sort locations based id
        raw_locations.sort(key=lambda x: x[1], reverse=True)

        # count multiple mentions
        for i, location in enumerate(raw_locations):
            positions = [raw_locations[i][5]]

            for alt in raw_locations[i + 1:]:
                if location[1] == alt[1]:
                    positions.append(alt[5])

            location[5] = min(positions)
            location[6] = len(positions)
            unique_locations.append(location)
            i += len(positions) - 1

        # sort locations based on size/area
        unique_locations.sort(key=lambda x: x[4], reverse=True)

        # highest frequency is used for normalization
        max_n = 0

        # check entailment of locations based on the bounding box
        for i, location in enumerate(unique_locations):
            for alt in raw_locations[i + 1:]:
                if alt[3][0] >= location[2][0] >= alt[3][1] and alt[3][2] >= location[2][1] >= alt[3][3]:
                    # We prefer more specific mentions, therefor we a fraction of the parent's number of mentions
                    location[6] += alt[6] / 0.8
            max_n = max(max_n, location[6])

        for location in unique_locations:
            # calculate score based on position in text (inverted pyramid) and the number of mentions
            score = weights[0] * (document.get_len() - location[5]) / document.get_len() + weights[1] * location[
                6] / max_n
            if score > 0:
                score /= weights_sum
            # new the last index holds the candidate wrapper object
            ca = location[7]
            ca.set_score(score)
            ranked_locations.append(ca)
            #ranked_locations.append((location[0], score))


        # NEW
        ranked_locations.sort(key=lambda x: x.get_score(), reverse=True)
        return ranked_locations

    def _evaluate_dates(self, document):
        """
        Calculate a confidence score for extracted time candidates.

        :param document: The parsed document.
        :type document: Document
        :param date_list: List of date candidates.
        :type date_list: [String, Integer]

        :return: A list of ranked candidates
        """

        ranked_candidates = []
        weights = self.weights[1]
        weights_sum = sum(weights)

        # fetch the date the article was published as a reference date
        reference = self.calendar.parse(document.get_date() or '')

        oCandidates = document.get_candidates('EnvironmentExtractorNeDates')
        for candidateO in oCandidates:

            candidate = candidateO.get_raw()
            # translate date strings into date objects
            # date_str = ' '.join([t[0] for t in candidate[0]])
            date_str = ' '.join([t['originalText'] for t in candidate])
            # Skip 'now' because its often part of a newsletter offer or similar
            if date_str.lower().strip() == 'now':
                continue
            parse = self.calendar.parse(date_str, reference[0])
            if parse[1] > 0:
                ranked_candidates.append([candidate[0], candidateO.get_sentence_index(), parse[0], parse[1], 1, candidateO])

        ranked_candidates.sort(key=lambda x: x[2])

        # Similar to the frequency used for locations we count similar date mentions.
        # Dates are considered related if they differ at most 24h (time_delta).
        max_n = 0
        for index, candidate in enumerate(ranked_candidates):
            for neighbour in ranked_candidates[index + 1:]:
                if (time.mktime(neighbour[2]) - time.mktime(candidate[2])) <= self.time_dela:
                    candidate[4] += 1
                    neighbour[4] += 1
            max_n = max(max_n, candidate[4])

        # Calculate the scores
        for candidate in ranked_candidates:
            # Position is the first parameter used scoring following the inverted pyramid
            score = weights[0] * (document.get_len() - candidate[1]) / document.get_len()

            if candidate[3] == 1:
                # Add a constant value if string contains a date
                score += weights[1]
            elif candidate[3] == 2:
                # Add a constant value if string contains a time
                score += weights[2]
            else:
                # String contains date and time
                score += weights[1] + weights[2]

            # Number of similar dates is also included as it indicates relevance
            score += weights[3] * (candidate[4] / max_n)

            if score > 0:
                score /= weights_sum
            #candidate[1] = score
            # 5 is the wrapper object
            candidate[5].set_score(score)

        # format bugfix - take the raw information and form a standardized parts format
        # this is the same format as the nlp tree leafs
        # TODO: add the leaf itself instead of rebuilding the same structure
        # TODO: do this already in _extract_candidates to speed it up
        for candidate in oCandidates:
            raw = candidate.get_raw()
            parts = []
            for old_part in raw:
                parts.append(({'nlpToken': old_part}, old_part['pos']))
            candidate.set_parts(parts)


        oCandidates.sort(key=lambda x: x.get_score(), reverse=True)
        return oCandidates


    # This function is not "scaning" by a pattern: it fetches the pos tag for a word, by walking over all tokens
    def _fetch_pos(self, pos, pattern):
        """
        This function scans a tokenized sentence with POS-labels for a token sequence

        :param pos: sentence with POS-labels
        :type pos: [(String, String)]
        :param pattern: The tokens without POS-labels
        :type pattern: [String]

        :return: The tokens of the pattern with POS-labels
        """

        for i, token in enumerate(pos):
            if token[0] == pattern[0] and [t[0] for t in pos[i:i + len(pattern)]] == pattern:
                rt = pos[i:i + len(pattern)]
                return rt
        return []
