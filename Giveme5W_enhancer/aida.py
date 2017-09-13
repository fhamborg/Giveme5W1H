import requests
import datetime
import time
from .abs_enhancer import AbsEnhancer, target

# default service is calling  https://www.ambiverse.com/pricing/
# at the time of writing there is a request limit 60 API calls per minute/1K API calls per month
# setup your own server for request

class Aida(AbsEnhancer):
    def __init__(self, questions, url=None):
        self._questions = questions

        self._url = url
        self._last_request = None
        if not url:
            self._url = 'https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate'
            self._limit_request_rate = True

    def process(self, document):
        # make sure there is just one call per second, if rate is limited
        if self._limit_request_rate:
            now = datetime.datetime.now()
            if self._last_request:
                time_since_last = (now - self._last_request).total_seconds()
                if time_since_last > 2:
                    time.sleep(2-time_since_last)

        r = requests.post(self._url, data={'text': document.get_fullText()})
        if self._limit_request_rate:
            self._last_request = datetime.datetime.now()

        o = r.json()
        document.set_enhancement('aida', o)

    def enhance(self, document):
        return None
        # TODO mapper
        # candidates = document.get_answers().get(self._question)
