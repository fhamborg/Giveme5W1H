import time
from .abs_extractor import AbsExtractor
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from parsedatetime import parsedatetime as pdt


class EnvironmentExtractor(AbsExtractor):
    """
    The EnvironmentExtractor tries to extract the location and time the event happened.
    """

    # weights used in the candidate evaluation:
    # ((position, frequency), (position, date, time, frequency))
    weights = ((1, 1), (2, 2, 1, 1))

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

        self.geocoder = Nominatim(domain=host, timeout=2)

        # init calender object for date resolution
        self.calendar = pdt.Calendar()

        # date strings like 'monday' can denote dates in the future as well as in the past
        # in most cases an article describes an event in the past
        self.calendar.ptc.DOWParseStyle = -1            # prefer day in the past for 'monday'
        self.calendar.ptc.CurrentDOWParseStyle = True   # prefer reference date if its the same weekday
        self.time_dela = 129600                         # 32h in seconds

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
        
        document.set_answer('where', self._filter_duplicates(locations, False))
        document.set_answer('when', self._filter_duplicates(dates, False))

    def _extract_candidates(self, document):
        """
        Extracts all locations, dates and times.

        :param document: The Document object to parse
        :type document: Document

        :return: A Tuple containing a list of locations and a list of dates.
        """

        # fetch results of the NER
        ner_tags = document.get_ner()
        locations = []
        dates = []
        last_date = None

        for i, entity in enumerate(ner_tags):
            # phrase_range=2 allows entities to be separate by single tokens, this is common for locations and dates
            # i.e. 'London, England' or 'October 13, 2015'.
            for candidate in self._extract_entities(ner_tags[i], ['LOCATION', 'TIME', 'DATE'], inverted=True,
                                                    phrase_range=2, groups={'TIME': 'TIME+DATE', 'DATE': 'TIME+DATE'}):

                if candidate[1] == 'LOCATION':
                    # look-up geocode in Nominatim
                    location = self.geocoder.geocode(' '.join(candidate[0]))
                    if location is not None:
                        locations.append((candidate[0], location, i))
                elif candidate[1] == 'TIME':
                    # If a date was already mentioned combine it with the mentioned time
                    if last_date is not None:
                        dates.append((last_date + candidate[0], i))
                    else:
                        dates.append((candidate[0], i))
                elif candidate[1] == 'DATE':
                    dates.append((candidate[0], i))
                    last_date = candidate[0]
                else:
                    # String includes date and time
                    dates.append((candidate[0], i))

        document.set_candidates('EnvironmentExtractorNeDates', dates)
        document.set_candidates('EnvironmentExtractorNeLocatios', locations)
        #return locations, dates

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

        for location in document.get_candidates('EnvironmentExtractorNeLocatios'):
            # fetch the boundingbox: (min lat, max lat, min long, max long)
            bb = location[1].raw['boundingbox']

            # use the vincenty algorithm to calculate the covered area
            area = int(vincenty((bb[0], bb[2]), (bb[0], bb[3])).meters) \
                * int(vincenty((bb[0], bb[2]), (bb[1], bb[2])).meters)
            for i in range(4):
                bb[i] = float(bb[i])
            raw_locations.append([location[0], location[1].raw['place_id'],
                                  location[1].point, bb, area, location[2], 0])

        # sort locations based id
        raw_locations.sort(key=lambda x: x[1], reverse=True)

        # count multiple mentions
        for i, location in enumerate(raw_locations):
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
            score = weights[0] * (document.get_len() - location[5])/document.get_len() + weights[1] * location[6]/max_n
            if score > 0:
                score /= weights_sum
            ranked_locations.append((location[0], score))

        ranked_locations.sort(key=lambda x: x[1], reverse=True)
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

        # translate date strings into date objects
        for candidate in  document.get_candidates('EnvironmentExtractorNeDates'):
            date_str = ' '.join(candidate[0])
            # Skip 'now' because its often part of a newsletter offer or similar
            if date_str.lower().strip() == 'now':
                continue
            parse = self.calendar.parse(date_str, reference[0])
            if parse[1] > 0:
                ranked_candidates.append([candidate[0], candidate[1], parse[0], parse[1], 1])

        ranked_candidates.sort(key=lambda x: x[2])

        # Similar to the frequency used for locations we count similar date mentions.
        # Dates are considered related if they differ at most 36h (time_delta).
        max_n = 0
        for index, candidate in enumerate(ranked_candidates):
            for neighbour in ranked_candidates[index+1:]:
                if (time.mktime(neighbour[2]) - time.mktime(candidate[2])) <= self.time_dela:
                    candidate[4] += 1
                    neighbour[4] += 1
            max_n = max(max_n, candidate[4])

        # Calculate the scores
        for candidate in ranked_candidates:
            # Position is the first parameter used scoring following the inverted pyramid
            score = weights[0] * (document.get_len() - candidate[1])/document.get_len()

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
            score += weights[3] * (candidate[4]/max_n)

            if score > 0:
                score /= weights_sum
            candidate[1] = score

        ranked_candidates = [(c[0], c[1]) for c in ranked_candidates]
        ranked_candidates.sort(key=lambda x: x[1], reverse=True)
        return ranked_candidates



