import datetime
import math

from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from parsedatetime import parsedatetime as pdt

from extractor.candidate import Candidate
from extractor.extractors.abs_extractor import AbsExtractor
from extractor.tools.timex import Timex
from tools.cache_manager import CacheManager


class EnvironmentExtractor(AbsExtractor):
    """
    The EnvironmentExtractor tries to extract the location and time the event happened.
    """

    one_minute_in_s = 60
    one_hour_in_s = one_minute_in_s * 60
    one_day_in_s = one_hour_in_s * 24
    two_days_in_s = one_day_in_s * 2
    one_month_in_s = one_day_in_s * 30

    # used for normalisation of time
    time_norm_min = math.log(one_minute_in_s)
    time_norm_max = math.log(one_month_in_s * 12)  # a year
    time_norm_delta = time_norm_max - time_norm_min

    # used for normalisation of area (in square meters)
    area_norm_min = math.log(225)  # roughly one small building
    area_norm_max = math.log(530000000000) # mean size of all countries (CIA factbook)
    area_norm_delta = area_norm_max - area_norm_min

    def __init__(self, weights=((0.37, 0.3, 0.3, 0.03), (0.24, 0.16, 0, 0.4, 0.2)), phrase_range_location: int = 3,
                 time_range: int = 86400, host='nominatim.openstreetmap.org', skip_when: bool = False,
                 skip_where: bool = False):
        """
        Init the Nominatim connection as well as the calender object used for date interpretation.

        When & Where are independent from each other,
        you can enable/disable them to increase execution speed

        :param weights: Weights used to evaluate answer candidates.
        :type weights: ((Float, Float), (Float, Float, Float)), weights used in the candidate scoring:
        ((position, frequency, entailment, accurate), (position, frequency, entailment, distance_from_publisher_date, accurate))
        :param host: Address of the Nominatim host
        :type host: String
        """

        # set weights
        self.weights = weights

        # init db connection used for location resolution
        self.geocoder = Nominatim(domain=host, timeout=8)

        # init calender object for date resolution
        self.calendar = pdt.Calendar()

        # date strings like 'monday' can denote dates in the future as well as in the past
        # in most cases an article describes an event in the past
        self.calendar.ptc.DOWParseStyle = -1  # prefer day in the past for 'monday'
        self.calendar.ptc.CurrentDOWParseStyle = True  # prefer reference date if its the same weekday
        self.time_delta = time_range  # 24h in seconds

        self._phrase_range_location = phrase_range_location
        self._cache_nominatim = CacheManager.instance().get_cache('../examples/caches/Nominatim')

        self._skip_when = skip_when
        self._skip_where = skip_where

    def _evaluate_candidates(self, document):

        if self._skip_where is False:
            locations = self._evaluate_locations(document)
            locations_clean = self._filter_candidate_dublicates(locations)
            document.set_answer('where', locations_clean)

        if self._skip_when is False:
            dates = self._evaluate_timex_dates(document)
            locations_dates = self._filter_candidate_dublicates(dates)
            document.set_answer('when', locations_dates)

    def _extract_timex_candidates(self, tokens):
        timex_dates = {}

        for cur_token in tokens:
            if 'timex' in cur_token:
                timex_obj = cur_token['timex']
                timex_id = timex_obj['tid']
                # timex_date = timex_obj['value']

                # check whether the timed_id was already found previously
                if timex_id in timex_dates:
                    # update the tokens list
                    found_candidate_token_list = timex_dates[timex_id]
                    found_candidate_token_list.append(cur_token)
                else:
                    found_candidate_token_list = [cur_token]
                    timex_dates[timex_id] = found_candidate_token_list

        candidate_list = []
        for timex_id in timex_dates:
            timex_token_list = timex_dates[timex_id]
            candidate_list.append((timex_token_list, 'TIMEX'))

        return candidate_list

    def _extract_candidates(self, document):
        """
        Extracts all locations, dates and times.

        :param document: The Document object to parse
        :type document: Document

        :return: A Tuple containing a list of locations and a list of dates.
        """

        # fetch results of the NER
        locations = []
        timex_candidates = []

        tokens = document.get_tokens()

        for i, sentence in enumerate(tokens):
            # phrase_range=2 allows entities to be separate by single tokens, this is common for locations and dates
            # i.e. 'London, England' or 'October 13, 2015'.
            for candidate in self._extract_entities(sentence, ['LOCATION'], inverted=True,
                                                    phrase_range=self._phrase_range_location,
                                                    accessor='ner'):

                # look-up geocode in Nominatim
                # try:
                location_array = [t['originalText'] for t in candidate[0]]
                location_string = ' '.join(location_array)

                # there is an exception if request went wrong,
                # None values are not cached,
                # therefore -1 is used to cache requests without result
                location = self._cache_nominatim.get(location_string)
                if location is None:
                    location = self.geocoder.geocode(location_string)

                    if location is None:
                        self._cache_nominatim.cache(location_string, -1)
                    else:
                        self._cache_nominatim.cache(location_string, location)
                if location == -1:
                    location = None

                if location is not None:
                    # fetch pos and append to candidates
                    ca = Candidate()

                    ca.set_raw(candidate[0])
                    ca.set_sentence_index(i)
                    # that's for the internal evaluation
                    ca.set_calculations('openstreetmap_nominatim', location)
                    # that's for the output
                    ca.set_enhancement('openstreetmap_nominatim', location.raw)

                    locations.append(ca)
                    # print('TRUE: ' + location_string)
                # else:
                # print('FALSE: ' + location_string)

                # except GeocoderServiceError as e:
                #    logging.getLogger('GiveMe5W').error('openstreetmap_nominatim: Where was not extracted ')
                #    logging.getLogger('GiveMe5W').error(str(e))

            # date candidate extraction using SUTime
            current_timex_candidates = self._extract_timex_candidates(sentence)
            for timex_candidate in current_timex_candidates:
                # some timex  have only a altValue field, this bugfix is ignoring them
                # gold_standard
                # 51bd183bdd5c2ea99cdc5f0dfe49feb816b0185371c8f30842549c33
                # 'altValue' (5223107824) -> '2016-11-11-WXX-5 INTERSECT PTXH'
                timex_date_value = timex_candidate[0][0]['timex'].get('value')
                if timex_date_value:
                    timex_obj = Timex.from_timex_text(timex_date_value)
                    if timex_obj:
                        ca = Candidate()
                        ca.set_raw(timex_candidate[0])
                        ca.set_sentence_index(i)
                        ca.set_calculations('timex', timex_obj)
                        ca.set_enhancement('timex', timex_obj.get_json())
                        timex_candidates.append(ca)

        document.set_candidates(self.get_id() + 'Locatios', locations)
        document.set_candidates(self.get_id() + 'TimexDates', timex_candidates);

    def _evaluate_locations(self, document):
        """
        Calculate a confidence score for extracted location candidates.

        :param document: The parsed document.
        :type document: Document

        :return: A list of evaluated and ranked candidates
        """
        raw_locations = []
        unique_locations = []
        ranked_locations = []
        weights = self.weights[0]
        weights_sum = sum(weights)
        max_area = 1

        for candidate in document.get_candidates(self.get_id() + 'Locatios'):
            # fetch the boundingbox: (min lat, max lat, min long, max long)
            parts = candidate.get_raw()
            location = candidate.get_calculations('openstreetmap_nominatim')
            bb = location.raw['boundingbox']

            # use the vincenty algorithm to calculate the covered area
            area = int(great_circle((bb[0], bb[2]), (bb[0], bb[3])).meters) * int(
                great_circle((bb[0], bb[2]), (bb[1], bb[2])).meters)
            for i in range(4):
                bb[i] = float(bb[i])
            raw_locations.append([parts, location.raw['place_id'], location.point, bb, area, 0, 0, candidate, 0])

            max_area = max(max_area, area)

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
        max_n = 1

        # number of entailments
        max_entailment = 1  # to avoid 0 division

        # check entailment of locations based on the bounding box
        for i, location in enumerate(unique_locations):
            for alt in raw_locations[i + 1:]:
                if alt[3][0] >= location[2][0] >= alt[3][1] and alt[3][2] >= location[2][1] >= alt[3][3]:
                    location[8] += 1
            max_n = max(max_n, location[6])
            max_entailment = max(max_entailment, location[8])

        for location in unique_locations:
            # calculate score based on position in text
            score = weights[0] * (document.get_len() - location[5]) / document.get_len()

            # frequency (based on entailment)
            score += weights[1] * (location[6] / max_n)

            # entailment
            score += weights[2] * (location[8] / max_entailment)

            # accuracy (ideally one minute only, max is one year) logarithmic
            normalized_area = (((math.log(location[4] + 1)) - EnvironmentExtractor.area_norm_min) /
                               EnvironmentExtractor.area_norm_delta)
            normalized_area = min(normalized_area, 1)
            normalized_area = max(normalized_area, 0)
            score += weights[3] * (1 - normalized_area)

            if score > 0:
                score /= weights_sum
            # new the last index holds the candidate wrapper object
            ca = location[7]
            ca.set_score(score)
            ranked_locations.append(ca)

        # NEW
        ranked_locations.sort(key=lambda x: x.get_score(), reverse=True)

        # Format Fix - mime tree structure
        for ranked in ranked_locations:
            raw_list = ranked.get_raw()
            parts = []
            for raw in raw_list:
                parts.append(({'nlpToken': raw}, raw['pos']))
            ranked.set_parts(parts)
        return ranked_locations

    def _evaluate_timex_dates(self, document):
        """
        Calculate a confidence score for extracted timex candidates.

        :param document: The parsed document.
        :type document: Document
        :param date_list: List of date candidates.
        :type date_list: [String, Integer]

        :return: A list of ranked candidates
        """
        scoring_candidates = []
        weights = self.weights[1]
        weights_sum = sum(weights)

        # fetch the date the article was published as a reference date
        tmp_struct_time_ref, throwaway = self.calendar.parse(document.get_date() or '')
        reference_date = datetime.datetime(*tmp_struct_time_ref[:6])

        oCandidates = document.get_candidates(self.get_id() + 'TimexDates')
        for candidateO in oCandidates:
            candidate = candidateO.get_raw()
            candidate_timex = candidateO.get_calculations('timex')
            # logging.getLogger('GiveMe5W').debug(candidate_timex)

            # first token, sentence index, time, number of similar dates, number of candidates that entail this one, candidateO
            scoring_candidate = [candidate[0], candidateO.get_sentence_index(), candidate_timex, 1, 1, candidateO]

            # add to list of candidates
            scoring_candidates.append(scoring_candidate)

        max_n_similar = 0
        max_n_entailment = 0

        for index, candidate in enumerate(scoring_candidates):
            candidate_timex = candidate[2]
            candidate_duration = candidate_timex.get_duration()

            neighbor_candidates_list = scoring_candidates[:index] + scoring_candidates[:index + 1]
            for neighbor_candidate in neighbor_candidates_list:
                neighbor_candidate_timex = neighbor_candidate[2]
                neighbor_candidate_duration = neighbor_candidate_timex.get_duration()

                # similar date check. Dates are considered related if they differ at most 24h (time_delta). we do this only for
                # date ranges that are at most 2 days long. that is because we are mostly interested in the day range, and
                # it also seems not useful to compare if two years are within a range of 24h.
                if abs(candidate_duration.total_seconds()) <= EnvironmentExtractor.two_days_in_s and abs(
                        neighbor_candidate_duration.total_seconds()) <= EnvironmentExtractor.two_days_in_s:
                    if abs((
                                   candidate_timex.get_start_date() - neighbor_candidate_timex.get_start_date()).total_seconds()) <= self.time_delta or \
                            abs((
                                        candidate_timex.get_end_date() - neighbor_candidate_timex.get_end_date()).total_seconds()) <= self.time_delta:
                        candidate[3] += 1

                # full entailment check: if a date X is entailed in another date Y, increase the frequency of X
                if candidate_timex.is_entailed_in(neighbor_candidate_timex):
                    candidate[4] += 1

            max_n_similar = max(max_n_similar, candidate[3])
            max_n_entailment = max(max_n_entailment, candidate[4])

        # Calculate the scores
        for candidate in scoring_candidates:
            # Position is the first parameter used scoring following the inverted pyramid
            score = weights[0] * (document.get_len() - candidate[1]) / document.get_len()

            # Number of similar dates is also included as it indicates relevance
            score += weights[1] * (candidate[3] / max_n_similar)

            # number of entailments
            score += weights[2] * (candidate[4] / max_n_entailment)

            # distance from publisher date
            distance_in_secs = candidate[2].get_min_distance_in_seconds_to_datetime(reference_date)
            normalized_distance_score = 1 - min(distance_in_secs / EnvironmentExtractor.one_month_in_s,
                                                1)  # we cut off after one month
            score += weights[3] * normalized_distance_score

            # accuracy (ideally one minute only, max is one year) logarithmic
            normalized_duration = (
                    (math.log(candidate[2].get_duration().total_seconds()) - EnvironmentExtractor.time_norm_min)
                    / EnvironmentExtractor.time_norm_delta)

            score += weights[4] * (1 - normalized_duration)

            if score > 0:
                score /= weights_sum

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
