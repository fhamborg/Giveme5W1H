import requests
import datetime
import time
from .abs_enhancer import AbsEnhancer

# default service is calling  https://www.ambiverse.com/pricing/
# at the time of writing there is a request limit 60 API calls per minute/1K API calls per month
# setup your own server for request

class Aida(AbsEnhancer):
    def __init__(self, questions, url=None):
        self._questions = questions
        self._last_request = None
        if not url:
            self._url = 'https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate'
            self._limit_request_rate = True
        else:
            self._url = url

    def get_enhancer_id(self):
        return 'aida'

    def process(self, document):
        # make sure there is just one call per second, if rate is limited
        if self._limit_request_rate:
            now = datetime.datetime.now()
            if self._last_request:
                time_since_last = (now - self._last_request).total_seconds()
                if 1 > time_since_last:
                    time.sleep(1)
                    # there can`t be a shorter sleep than one second.
                    # This makes tops 2 seconds per request

        r = requests.post(self._url, data={'text': document.get_full_text()})
        if self._limit_request_rate:
            self._last_request = datetime.datetime.now()

        o = r.json()
        document.set_enhancement(self.get_enhancer_id() , o)

    def process_data(self, process_data, character_offset):

        # there could be more than one mention per character_offset
        result = []
        for mention in process_data['mentions']:
            offset = mention['offset']
            length = mention['length']

            process_data_offset = (offset, offset+length)

            if self.is_overlapping(character_offset, process_data_offset):
                bestEntity = mention.get('bestEntity')
                bestEntityMetadata = None

                # some have no Entity in the dataset
                if bestEntity:
                    bestEntityMetadata = process_data['entityMetadata'][bestEntity['kbIdentifier']]

                # TODO: besides bestEntityMetadata there are more under all (sometimes)
                result.append({'mention': mention, 'bestEntityMetadata': bestEntityMetadata})
        return result

