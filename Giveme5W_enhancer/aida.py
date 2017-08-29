import requests
import datetime
import time



# default service is calling  https://www.ambiverse.com/pricing/
# at the time of writing there is a request limit 60 API calls per minute/1K API calls per month
# setup your own server for request

class Aida():

    def __init__(self, question, url=None):
        self._question = question
        self._url = url
        self._last_request = None
        if not url:
            self._url = 'https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate'
            self._limit_request_rate = True

    def enhance(self, document):
        candidates = document.get_answers().get(self._question)
        if candidates:
            for candidate in candidates:
                answer_text = candidate.get_parts_as_text()
                # assumption, there is no way to define a time with 2 characters -> 1am
                if answer_text and len(answer_text) > 2:
                    now = None

                    # make sure there is just one call per second, if rate is limited
                    if self._limit_request_rate:
                        now = datetime.datetime.now()
                        if self._last_request:
                            time_since_last = (now - self._last_request).total_seconds()
                            if time_since_last > 2:
                                time.sleep(2-time_since_last)

                    r = requests.post(self._url, data={'text': answer_text})
                    if self._limit_request_rate:
                        self._last_request = datetime.datetime.now()
                    #print(r.text())
                    o = r.json()
                    candidate.set_enhancement('aida', o)

