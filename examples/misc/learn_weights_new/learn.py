import datetime
import time
from itertools import product

from dateutil.relativedelta import relativedelta as rd
from geopy.distance import vincenty
from nltk import word_tokenize
from nltk.corpus import wordnet

from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler

from tools.cache_manager import CacheManager

fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'


class Learn(object):
    def __init__(self, lock, input_path, preprocessed_path, extractors, queue, combined_scorer=None, ):

        # load docs an extractor
        self._input_path = input_path
        self._pre_processed_path = preprocessed_path
        self._documents, self._extractor_object = self.load_documents(extractors, combined_scorer)

        self._extractors = extractors
        if self._extractors.get('environment'):
            self._geocoder = self._extractors.get('environment').geocoder
            self._calendar = self._extractors.get('environment').calendar
        else:
            self._geocoder = None
            self._calendar = None

        self._combined_scorer = combined_scorer
        # object to work on (holds the todos)
        self._queue = queue
        self._lock = lock

        self._cache_nominatim = CacheManager.instance().get_cache('../examples/caches/Nominatim')
        self._cache_ngd = CacheManager.instance().get_cache('../examples/caches/NGD')



    def cmp_text(self, annotation, candidate):
        """
        Compare the retrieved answer with the annotation using WordNet path distance.

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

    def cmp_date(self, annotation, candidate):
        """
        Compare the retrieved answer with the annotation by calculating the time difference in seconds.

        "Beide Datum - das kleiner datum das genau in der mitte liegt -
        "Datum in der mitten nutzen
        "Datum, die Zeit Reibschreibe?

        :param annotation: The correct Answer
        :type annotation: (time.struct_time, Integer)
        :param candidate: The retrieved Answer
        :type candidate: [String]

        :return: Float
        """

        t = self._calendar.parse(annotation)
        if t[1] == 0:
            return -1
        elif candidate is None:
            # no answer was extracted
            return -2

        strings = []
        for candidatepart in candidate:
            strings.append(candidatepart[0])
        c_time = self._calendar.parse(' '.join(strings))

        if c_time[1] == 0:
            # one of the answers couldn't be parsed
            return -3

        a = time.mktime(t[0])
        b = time.mktime(c_time[0])

        return abs(a - b)

    def nominatim(self, candidate):

        if candidate is None:
            return -1

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

    def cmp_location(self, annotation, candidate):
        """
        Compare the retrieved answer with the annotation using geocoding and comparing the real world distance.

        :param annotation: The geocoded correct Answer
        :type annotation: Location
        :param candidate: The retrieved Answer
        :type candidate: Sting

        :return: Float
        """

        annotation = self.nominatim(annotation)
        if annotation == -1:
            # annotation is None or the annotation could'nt be parsed
            return -1
        elif candidate is None:
            # no answer was extracted
            return -2

        location = self.nominatim(candidate)
        if location == -1:
            # retrieved answer couldn't be parsed
            return -3


        return vincenty(annotation.point, location.point).kilometers

    def load_documents(self, extractors, combined_scorer):
        inputPath = path(self._input_path)
        preprocessedPath = path(self._pre_processed_path)

        # Setup
        if combined_scorer is not None:
            _combined_scorers = [combined_scorer]
        else:
            _combined_scorers = []
        extractor_object = FiveWExtractor(extractors=list(extractors.values()), combined_scorers=_combined_scorers)

        # Put all together, run it once, get the cached document objects
        docments = (
            # initiate the newsplease file handler with the input directory
            Handler(inputPath)
                # set a path to save an load preprocessed documents
                .set_preprocessed_path(preprocessedPath)
                # limit the the to process documents (nice for development)
                .set_limit(1)
                # add an optional extractor (it would do basically just copying without...)
                .set_extractor(extractor_object)
                # saves all document objects for further programming
                .preload_and_cache_documents()
                # executing it
                .process().get_documents()
        )

        return docments, extractor_object

    def _cmp_helper(self, scoring, question, answer, annotations, weights, result):
        # TODO: use named entity, if any
        score = -1
        # check if there is an annotaton and an answer
        if answer and question in annotations and len(annotations[question]) > 0:
            #topAnswer = answers[question][0].get_parts_as_text()
            for annotation in annotations[question]:
                if len(annotation) > 2:
                    topAnnotation = annotation[2]
                    if topAnnotation:
                        tmp_score = scoring(topAnnotation, answer)
                        score = max(tmp_score, score)
        result[question] = (question, weights, score)

    def _log_progress(self, queue, documents, start, end):
        count = queue.get_queue_count()
        doc_count = len(documents)

        print(queue.get_id() + ':Combinations: ' + str(count))
        print(queue.get_id() + ':There are ' + str(count * doc_count) + ' steps to go (docs * combinations)')
        if (start and end):
            time_range = (end - start).total_seconds()
            time_range = time_range * count
            # No proper average this is very rough
            print(queue.get_id() + ':Rough estimated time left:' + str(fmt.format(rd(seconds=time_range))))

    def process(self):
        # grab utilities to parse dates and locations from the EnvironmentExtractor


        self._log_progress(self._queue, self._documents, None, None)
        # make sure caller can read that...
        time.sleep(5)

        _pre_extracting_parameters_id = None
        while True:
            next_item = self._queue.next()
            if next_item is not None:
                if _pre_extracting_parameters_id:

                    if _pre_extracting_parameters_id != next_item['extracting_parameters_id']:
                        print("reset candidates - extracting values changed")
                        for document in self._documents:
                            document.reset_candidates

                _pre_extracting_parameters_id = next_item['extracting_parameters_id']

                # adjust weights
                weights = next_item['scoring_parameters']['weights']

                if self._extractors.get('action'):
                    #
                    self._extractors['action'].weights = (weights[0], weights[1], weights[2])

                if self._extractors.get('environment'):
                    # time
                    self._extractors['environment'].weights = (
                    (weights[0], weights[1]), (weights[0], weights[1], weights[2], weights[3], weights[4]))

                if self._extractors.get('cause'):
                    # cause - (position, conjunction, adverb, verb)
                    self._extractors['cause'].weights = (weights[0], weights[1], weights[2], weights[3])

                if self._extractors.get('method'):
                    # method - (position, frequency)
                    self._extractors['method'].weights = (weights[0], weights[1])

                combination_start_stamp = datetime.datetime.now()
                # run for all documents
                for document in self._documents:

                    #try:
                    self._extractor_object.parse(document)
                    #except socket.timeout:
                    #    print('online service (prob nominatim) did`t work, we ignore this')

                    annotation = document.get_annotations()
                    answers = document.get_answers()

                    #
                    # Extractors are based on their naming Cause, Method etc.
                    # answer(and their questions) have a very different structure
                    # Therefore the following lines are simple copy&paste to reorganise
                    # from one the the other format
                    #

                    result = {}

                    extractor = self._extractors.get('cause')
                    if extractor:
                        question = 'why'
                        if question in answers and len(answers[question]) > 0:
                            used_weights = extractor.weights
                            top_answer = answers[question][0].get_parts_as_text()
                            self._cmp_helper(self.cmp_text, question, top_answer, annotation, used_weights, result)

                    extractor = self._extractors.get('action')
                    if extractor:
                        used_weights = extractor.weights
                        question = 'what'
                        if question in answers and len(answers[question]) > 0:
                            top_answer = answers[question][0].get_parts_as_text()
                            self._cmp_helper(self.cmp_text,'what', top_answer, annotation, used_weights, result)

                        question = 'who'
                        if question in answers and len(answers[question]) > 0:
                            top_answer = answers[question][0].get_parts_as_text()
                            self._cmp_helper(self.cmp_text,question, top_answer, annotation, used_weights, result)

                    extractor = self._extractors.get('method')
                    if extractor:
                        used_weights = extractor.weights
                        question = 'how'
                        if question in answers and len(answers[question]) > 0:
                            top_answer = answers[question][0].get_parts_as_text()
                            self._cmp_helper(self.cmp_text,question, top_answer, annotation, used_weights, result)

                    extractor = self._extractors.get('environment')
                    if extractor:
                        used_weights = extractor.weights
                        question = 'when'
                        if question in answers and len(answers[question]) > 0:
                            top_answer = answers[question][0].get_parts_as_text()
                            self._cmp_helper(self.cmp_date,question, top_answer, annotation, used_weights, result)

                        question = 'where'
                        if question in answers and len(answers[question]) > 0:
                            top_answer = answers[question][0].get_parts_as_text()
                            self._cmp_helper(self.cmp_location, question, top_answer, annotation, used_weights, result)

                    # done save it to the result
                    self._queue.resolve_document(next_item, document.get_document_id(), result)

                combination_end_stamp = datetime.datetime.now()
                self._queue.pop(persist=True)
                self._log_progress(self._queue, self._documents, combination_start_stamp, combination_end_stamp)
            else:
                print('done')
                break
