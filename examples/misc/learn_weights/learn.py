import datetime
import logging
import math
import time
from itertools import product
from threading import Thread

import dateutil.parser

from dateutil.relativedelta import relativedelta as rd
from geopy.distance import great_circle
from nltk import word_tokenize, metrics
from nltk.corpus import wordnet

from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler
from misc.learn_weights.metrics.normalized_google_distance import NormalizedGoogleDistance
from misc.learn_weights.metrics.wmd import Wmd
from tools.cache_manager import CacheManager
import nltk
from nltk.metrics.distance        import edit_distance

class Worker(Thread):
    def __init__(self, queue):
        ''' Constructor. '''
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            _learn = self._queue.get()
            _learn.process()
            self._queue.task_done()


class Learn(object):
    """
    Wrapper class to learn weights and parameter.
    A lock object must be shared to ensure proper usage of caches and online resources.

    """
    one_minute_in_s = 60
    one_hour_in_s = one_minute_in_s * 60
    one_day_in_s = one_hour_in_s * 24
    two_days_in_s = one_day_in_s * 2
    one_month_in_s = one_day_in_s * 30

    # used for normalisation of time
    a_min = math.log(one_minute_in_s)
    a_max = math.log(one_month_in_s)  # a month
    a_min_minus_max = (a_max - a_min)

    def __init__(self, lock, input_path, preprocessed_path, extractors, queue, combined_scorer=None,
                 sampling='training', ignore_extractor=None, persit_steps=False):
        # load docs and extractor
        self._input_path = input_path
        self._pre_processed_path = preprocessed_path
        self._documents, self._extractor_object, self._combined_scorer = self.load_documents(extractors,
                                                                                             combined_scorer, sampling)

        self._extractors = extractors
        # removes extractors from list, if weights are not changing (for combined scoring)
        if ignore_extractor:
            for ignore in ignore_extractor:
                del self._extractors[ignore]
        if self._extractors.get('environment'):
            self._geocoder = self._extractors.get('environment').geocoder
            self._calendar = self._extractors.get('environment').calendar
        else:
            self._geocoder = None
            self._calendar = None

        # object to work on (holds the todos)
        self._queue = queue
        self._lock = lock

        self._cache_nominatim = CacheManager.instance().get_cache('../examples/caches/Nominatim')

        self._log = logging.getLogger('GiveMe5W')
        # self._cache_ngd = CacheManager.instance().get_cache('../examples/caches/NGD')
        # self._ngd = NormalizedGoogleDistance()
        self._wmd = Wmd()
        self._sampling = sampling
        self._persit_steps = persit_steps

    def cmp_text_ngd(self, annotation, candidate, entire_annotation):
        """ result is a distance from 0..N 0 = similar,
            (at the time of writing) greater 4 is absolute not correlated
        """
        result = self._ngd.get_distance(annotation, candidate)
        return result

    def cmp_text_wmd(self, annotation, candidate, entire_annotation):
        """
        """
        result = self._wmd.get_distance(annotation, candidate)
        return result

    def cmp_text_edit_distance(self, annotation, candidate, entire_annotation):
        """
        """
        result = edit_distance(annotation, candidate)
        return result

    def cmp_text_word_net(self, annotation, candidate, entire_annotation):
        """
        Compare the retrieved answer with the annotation using WordNet path distance.

        THIS IS VERY SLOW, RESULTS ARE NOT CACHED

        :param annotation: The correct Answer
        :type annotation: String
        :param candidate: The retrieved Answer
        :type candidate: [String, String]

        :return: Float
        """

        if annotation is None or annotation is 'NULL':
            # annotation is NULL
            return -1
        elif candidate is None:
            # no answer was extracted
            return -2

        # fetch synsets for both answers
        self._lock.acquire()
        syn_a = [wordnet.synsets(t) for t in word_tokenize(annotation)]
        syn_b = [wordnet.synsets(t[0]) for t in candidate]

        # drop tokens without synsets
        syn_a = [syn for syn in syn_a if len(syn) > 0]
        syn_b = [syn for syn in syn_b if len(syn) > 0]
        self._lock.release()

        if not any(syn_a) or not any(syn_b):
            # no synsets were found for one of the answers!
            return -3

        score = 0
        max_b = [0] * len(syn_b)

        self._lock.acquire()
        for i in range(len(syn_a)):
            max_a = 0
            for j in range(len(syn_b)):
                sim = max(list((wordnet.path_similarity(a, b) or 0) for a, b in product(syn_a[i], syn_b[j])) or [0])
                max_a = max(sim, max_a)
                max_b[j] = max(max_b[j], sim)

            score += max_a
        score += sum(max_b)
        self._lock.release()
        return score / len(syn_a) + len(syn_b)

    def cmp_date_timex(self, annotation, candidate, entire_annotation):
        """
        result is a distance from 0..1 0 = same point in time, 1 (a_max) a month or more apart
        :param annotation:
        :param candidate:
        :param entire_annotation:
        :return:
        """
        if candidate:
            if len(entire_annotation) > 3:
                parsed = entire_annotation[3].get('parsed')
                if parsed is None:
                    return -2
                parsed = dateutil.parser.parse(parsed)

            else:
                # there is no way to compare these dates without a proper date annotation
                return -2

            start = dateutil.parser.parse(candidate['start_date'])
            end = dateutil.parser.parse(candidate['end_date'])

            timespan = end - start
            timespan_in_sec = timespan.total_seconds()

            center_timestamp = start + datetime.timedelta(seconds=(timespan_in_sec / 2))

            distance_of_anno_and_extracted = abs((center_timestamp - parsed).total_seconds())

            normalized_duration = (math.log(distance_of_anno_and_extracted) - Learn.a_min) / Learn.a_min_minus_max
            return normalized_duration
        else:
            return -1

    def nominatim(self, candidate):

        if candidate is None:
            return -1

        location = self._cache_nominatim.get(candidate)
        if location is not None:
            return location

        self._lock.acquire()

        location = self._geocoder.geocode(candidate)
        if location is None:
            # According to old comments None is returned for not found
            # None can`t be cached (this is flag for something went wrong no cache, do it again etc..)
            location = -1

        self._cache_nominatim.cache(candidate, location)
        location = location

        self._lock.release()

        return location

    def cmp_location(self, annotation, candidate, entire_annotation):
        """
        Compare the retrieved answer with the annotation using geocoding and comparing the real world distance.
        returns distance in kilometers
        :param annotation: The geocoded correct Answer
        :type annotation: Location
        :param candidate: The retrieved Answer
        :type candidate: Sting

        :return: Float
        """
        if annotation is None:
            # annotation is None
            return -1

        annotation = self.nominatim(annotation)
        if annotation == -1:
            # or the annotation could'nt be parsed
            return -3
        elif candidate is None:
            # no answer was extracted
            return -4

        location = self.nominatim(candidate)
        if location == -1:
            # retrieved answer couldn't be parsed
            return -3

        # 20039 is half of the earth circumference alon equator.
        # We ignore the fact that the earth not perfect round
        return great_circle(annotation.point, location.point).kilometers

    def load_documents(self, extractors, combined_scorer, sampling):
        inputPath = path(self._input_path)
        preprocessedPath = path(self._pre_processed_path)

        # Setup
        if combined_scorer is not None:
            _combined_scorers = [combined_scorer]
        else:
            _combined_scorers = []
        extractor_object = FiveWExtractor(extractors=list(extractors.values()), combined_scorers=_combined_scorers)

        # Put all together, run it once, get the cached document objects
        documents = (
            # initiate the newsplease file handler with the input directory
            Handler(inputPath)
                # set a path to save an load preprocessed documents
                .set_preprocessed_path(preprocessedPath)
                # limit the the to process documents (nice for development)
                # .set_limit(1)
                # add an optional extractor (it would do basically just copying without...)
                .set_sampling(sampling)
                .set_extractor(extractor_object)
                # saves all document objects for further programming
                .preload_and_cache_documents()
                # executing it
                .process().get_documents()
        )

        return documents, extractor_object, combined_scorer

    def _cmp_helper_min(self, scoring, question, answer, annotations, weights, result):
        # TODO: use named entity, if any
        scores = []
        # check if there is an annotaton and an answer
        if answer and question in annotations and len(annotations[question]) > 0:
            # topAnswer = answers[question][0].get_parts_as_text()
            for annotation in annotations[question]:
                if len(annotation) > 2:
                    topAnnotation = annotation[2]
                    if topAnnotation:
                        tmp_score = scoring(topAnnotation, answer, annotation)
                        scores.append(tmp_score)

        no_error_values = [x for x in scores if x is not None and x >= 0]
        if len(no_error_values) > 0:
            smallest_none_error = min(no_error_values)
            result[question] = (question, weights, smallest_none_error, scores)
        else:
            # no annotation
            result[question] = (question, weights, -1, scores)

    def _log_progress(self, queue, documents, start, end):
        count = queue.get_queue_count()
        doc_count = len(documents)

        self._log.info(queue.get_id() + ':Combinations: ' + str(count))
        self._log.info(queue.get_id() + ':There are ' + str(count * doc_count) + ' steps to go (docs * combinations)')
        if (start and end):
            time_range = (end - start).total_seconds()
            time_range = time_range * count
            # No proper average this is very rough
            fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'
            self._log.info(queue.get_id() + ':Rough estimated time left:' + str(fmt.format(rd(seconds=time_range))))

    def process(self):

        self._log_progress(self._queue, self._documents, None, None)
        # make sure caller can read that...

        _pre_extracting_parameters_id = None
        while True:

            next_item = self._queue.next()
            if next_item is not None:
                if _pre_extracting_parameters_id:
                    if _pre_extracting_parameters_id != next_item['extracting_parameters_id']:
                        print("reset candidates - extracting values changed")
                        for document in self._documents:
                            document.reset_candidates()

                _pre_extracting_parameters_id = next_item['extracting_parameters_id']

                # adjust weights
                weights = next_item['scoring_parameters']['weights']

                if self._combined_scorer:
                    self._combined_scorer._weight = (weights[0],)
                else:

                    if self._extractors.get('action'):
                        #
                        self._extractors['action'].weights = (weights[0], weights[1], weights[2])

                    if self._extractors.get('environment'):
                        # time, location
                        self._extractors['environment'].weights = (
                            (weights[0], weights[1]), (weights[0], weights[1], weights[2], weights[3], weights[4]))

                    if self._extractors.get('environment_where'):
                        # location
                        self._extractors['environment_where'].weights = (
                            (weights[0], weights[1], weights[2], weights[3]), (-1, -1, -1, -1, -1))
                    if self._extractors.get('environment_when'):
                        # time
                        self._extractors['environment_when'].weights = (
                            (-1, -1), (weights[0], weights[1], weights[2], weights[3], weights[4]))

                    if self._extractors.get('cause'):
                        # cause - (position, conjunction, adverb, verb)
                        self._extractors['cause'].weights = (weights[0], weights[1], weights[2], weights[3])

                    if self._extractors.get('method'):
                        # method - (position, frequency)
                        self._extractors['method'].weights = (weights[0], weights[1], weights[2], weights[3])

                # run for all documents
                for i, document in enumerate(self._documents):

                    self._extractor_object.parse(document)

                    annotation = document.get_annotations()
                    answers = document.get_answers()

                    result = {}

                    if self._combined_scorer:
                        # Combined scoring is happening after candidate extraction
                        used_weights = self._combined_scorer._weight
                        question = 'how'
                        if 'how' in answers and len(answers[question]) > 0:
                            top_answer = answers[question][0].get_parts_as_text()
                        self._cmp_helper_min(self.cmp_text_edit_distance, question, top_answer, annotation, used_weights, result)
                    else:
                        extractor = self._extractors.get('cause')
                        if extractor:
                            question = 'why'
                            if question in answers and len(answers[question]) > 0:
                                used_weights = extractor.weights
                                top_answer = answers[question][0].get_parts_as_text()
                                self._cmp_helper_min(self.cmp_text_edit_distance, question, top_answer, annotation, used_weights,
                                                     result)

                        extractor = self._extractors.get('action')
                        if extractor:
                            used_weights = extractor.weights
                            question = 'what'
                            if question in answers and len(answers[question]) > 0:
                                top_answer = answers[question][0].get_parts_as_text()
                                self._cmp_helper_min(self.cmp_text_edit_distance, 'what', top_answer, annotation, used_weights,
                                                     result)

                            question = 'who'
                            if question in answers and len(answers[question]) > 0:
                                top_answer = answers[question][0].get_parts_as_text()
                                self._cmp_helper_min(self.cmp_text_edit_distance, question, top_answer, annotation, used_weights,
                                                     result)

                        extractor = self._extractors.get('method')
                        if extractor:
                            used_weights = extractor.weights
                            question = 'how'
                            if question in answers and len(answers[question]) > 0:
                                top_answer = answers[question][0].get_parts_as_text()
                                self._cmp_helper_min(self.cmp_text_edit_distance, question, top_answer, annotation, used_weights,
                                                     result)

                        extractor = self._extractors.get('environment_when')
                        if extractor:
                            used_weights = extractor.weights[1]
                            question = 'when'
                            if question in answers and len(answers[question]) > 0:
                                top_answer = answers[question][0].get_enhancement('timex')
                                self._cmp_helper_min(self.cmp_date_timex, question, top_answer, annotation,
                                                     used_weights, result)

                        extractor = self._extractors.get('environment_where')
                        if extractor:
                            question = 'where'
                            used_weights = extractor.weights[0]
                            if question in answers and len(answers[question]) > 0:
                                top_answer = answers[question][0].get_parts_as_text()
                                self._cmp_helper_min(self.cmp_location, question, top_answer, annotation, used_weights,
                                                     result)

                    # done save it to the result
                    self._queue.resolve_document(next_item, document.get_document_id(), result, i)

                self._queue.pop(persist=self._persit_steps)
            else:

                self._queue.persist()
                print('done')
                break
