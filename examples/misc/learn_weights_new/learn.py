import datetime
import socket
import time

from dateutil.relativedelta import relativedelta as rd

from extractor.extractor import FiveWExtractor
from extractor.root import path
from extractor.tools.file.handler import Handler
from extractor.tools.util import cmp_text, cmp_date, cmp_location

# Add path to allow execution though console
# sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-2]))
# from timeit import default_timer as timer
# core_nlp_host = 'http://localhost:9000'

fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'


class Learn(object):
    def __init__(self, input_path, preprocessed_path, extractors, queue, combined_scorer=None):
        self._input_path = input_path
        self._pre_processed_path = preprocessed_path
        self._extractors = extractors
        self._combined_scorer = combined_scorer
        self._queue = queue
        self._documents, self._extractor_object = self.load_documents(extractors, combined_scorer)

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
                .set_limit(50)
                # add an optional extractor (it would do basically just copying without...)
                .set_extractor(extractor_object)
                # saves all document objects for further programming
                .preload_and_cache_documents()
                # executing it
                .process().get_documents()
        )

        return docments, extractor_object

    def _cmp_text_helper(self, question, answers, annotations, weights, result):
        score = -1
        # check if there is an annotaton and an answer
        if question in annotations and question in answers and len(annotations[question]) > 0 and len(
                answers[question]) > 0:
            topAnswer = answers[question][0].get_parts_as_text()
            for annotation in annotations[question]:
                if len(annotation) > 2:
                    topAnnotation = annotation[2]
                    if topAnnotation and topAnswer:
                        tmp_score = cmp_text(topAnnotation, topAnswer)
                        score = max(tmp_score, score)
        result[question] = (question, weights, score)

    def _cmp_date_helper(self, question, answers, annotations, weights, calendar, result):
        score = -1
        # check if there is an annotaton and an answer
        if question in annotations and question in answers and len(annotations[question]) > 0 and len(
                answers[question]) > 0:
            topAnswer = answers[question][0].get_parts_as_text()
            for annotation in annotations[question]:
                if len(annotation) > 2:
                    topAnnotation = annotation[2]
                    if topAnnotation and topAnswer:
                        tmp_score = cmp_date(topAnnotation, topAnswer, calendar)
                        score = max(tmp_score, score)

        result[question] = (question, weights, score)

    def _cmp_location_helper(self, question, answers, annotations, weights, geocoder, result):
        score = -1
        # check if there is an annotaton and answer
        if question in annotations and question in answers and len(annotations[question]) > 0 and len(
                answers[question]) > 0:
            topAnswer = answers[question][0].get_parts_as_text()
            for annotation in annotations[question]:
                if len(annotation) > 2:
                    topAnnotation = annotation[2]
                    if topAnnotation and topAnswer:
                        tmp_score = cmp_location(topAnnotation, topAnswer, geocoder)
                        score = max(tmp_score, score)
        result[question] = (question, weights, score)

    def _log_progress(self, queue, documents, start, end):
        count = queue.get_queue_count()
        doc_count = len(documents)
        print('There are ' + str(count * doc_count) + ' steps to go')
        if (start and end):
            time_range = (end - start).total_seconds()
            time_range = time_range * count
            # No proper average this is very rough


            print('Rough estimated time left:' + str(fmt.format(rd(seconds=time_range))))

    def process(self):
        # grab utilities to parse dates and locations from the EnvironmentExtractor
        if self._extractors.get('environment'):
            geocoder = self._extractors.get('environment').geocoder
            calendar = self._extractors.get('environment').calendar

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

                    try:
                        self._extractor_object.parse(document)
                    except socket.timeout:
                        print('online service (prob nominatim) did`t work, we ignore this')

                    annotation = document.get_annotations()
                    answers = document.get_answers()

                    result = {}

                    if self._extractors.get('cause'):
                        self._cmp_text_helper('why', answers, annotation,
                                              [weights[0], weights[1], weights[2], weights[3]], result)
                    if self._extractors.get('action'):
                        self._cmp_text_helper('what', answers, annotation, [weights[0], weights[1], weights[2]], result)
                        self._cmp_text_helper('who', answers, annotation, [weights[0], weights[1], weights[2]], result)

                    if self._extractors.get('method'):
                        self._cmp_text_helper('how', answers, annotation, [weights[0], weights[1]], result)

                    # These two are tricky because of the used online services
                    if self._extractors.get('environment'):
                        self._cmp_date_helper('when', answers, annotation,
                                              [weights[0], weights[1], weights[2], weights[3]], calendar, result)

                    # try:
                    # cmp_location_helper('where', answers, annotation, [i, weights[1]], geocoder, result)
                    # except socket.timeout:
                    # print('online service (prob nominatim) did`t work, we ignore this')


                    # done save it to the result
                    self._queue.resolve_document(next_item, document.get_document_id(), result)

                combination_end_stamp = datetime.datetime.now()
                self._queue.pop(persist=True)
                self._log_progress(self._queue, self._documents, combination_start_stamp, combination_end_stamp)
            else:
                print('done')
                break
