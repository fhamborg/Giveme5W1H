import logging
import math

import requests
from lxml import html

from misc.learn_weights.metrics.abs_metric import AbsMetric


class NormalizedGoogleDistance(AbsMetric):
    """
    Normalized Google distance"
    https://de.wikipedia.org/wiki/Normalisierte_Google-Distanz

    this is a port from newsCluster
    """

    def __init__(self, *args, **kwargs):
        super(NormalizedGoogleDistance, self).__init__(*args, **kwargs)

        self._log_M = math.log(80580446510)

    def _get_de_hit_count(self, html_element):
        if html_element and len(html_element) > 0 and html_element[0].text:
            string = html_element[0].text.split()
            # remove thousand dots, if any
            len_result = len(string)
            if len_result == 2:
                # [number] Ergebnisse
                result = string[0]
            elif len_result == 3:
                # ungefähr [number] Ergebnisse
                result = string[1]
            else:
                logging.error('NormalizedGoogleDistance: count could not be extracted, assuming 0 results')
                return 1
        else:
            logging.error('NormalizedGoogleDistance: count could not be extracted, assuming 0 results')
            return 1

        # removing thousand dots and converting to int
        return int(result.replace(".", ""))

    def _request(self, candidates):
        # check cache
        cache_content = self._cache.get_complex(candidates)

        if cache_content is not None:
            return cache_content
        cookies = dict(CONSENT='YES+DE.de+20160407-02-0')
        # https://sites.google.com/site/tomihasa/google-language-codes
        result = requests.get('https://www.google.de/search', params={'q': " ".join(candidates), 'hl': 'de'},
                              cookies=cookies)
        tree = html.fromstring(result.content)

        if result is not None:
            html_element = tree.xpath(".//div[@id='resultStats']")
            if tree.attrib['lang'].startswith('de'):
                x = self._get_de_hit_count(html_element)
            else:
                logging.error(
                    'google may redirect to your country - you must implement your country specific _get_xx_hit_count')

            self._cache.cache_complex(candidates, x)

            return x
        else:
            # None results are not Cached, they result from connection errors
            return None

    def calculate_distance(self, candidates_a, candidates_b):
        """
        :param candidates_a:
        :param candidates_b:
        :return:
        """

        # special case two None, so this articles had no answer -> similar -> low distance
        if candidates_a is None and candidates_b is None:
            return 0

        # candidates_a
        x = self._request([candidates_a])

        # candidates_b
        y = self._request([candidates_b])

        # candidates_a & candidates_b
        xy = self._request([candidates_a, candidates_b])

        if x == 0 or y == 0 or xy == 0:
            # NGD is not defined here
            return None
        elif x is not None and y is not None and xy is not None:
            log_x = math.log(x)
            log_y = math.log(y)
            log_xy = math.log(xy)
            max_log_x_y = max(log_x, log_y)
            min_log_x_y = min(log_x, log_y)

            return (max_log_x_y - log_xy) / (self._log_M - min_log_x_y)
        else:
            logging.error('A: ' + candidates_a + '  B: ' + candidates_b)
            return None
