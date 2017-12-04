import logging
import os
import pickle
import sys
import threading
import time
from typing import List

from root import path
from tools.util import bytes_2_human_readable


class KeyValueCache(object):
    def __init__(self, cache_path):
        """
        :param cache_path: path to cache, must be relative to the root.py file
        """

        self.log = logging.getLogger('GiveMe5W')
        # resolve path relative to the path file
        self._cache_path = path(cache_path)
        # ad a meaningful extension
        self._cache_path = self._cache_path + '.prickle'

        self._cache = {}

        if cache_path and os.path.isfile(self._cache_path) and os.path.getsize(self._cache_path) > 0:
            # reload cache object form disc, if any
            with open(self._cache_path, 'rb') as ff:
                self._cache = pickle.load(ff)
                self.log.debug('KeyValueCache: ' + self._cache_path + ' restored')
                self.log_stats()
        else:
            self._cache = {}
        self._lock = threading.Lock()

    def log_stats(self):
        # size is not considering child's
        self.log.info(self._cache_path + ' entries: ' + str(len(self._cache)) + ' size: ' + bytes_2_human_readable(
            sys.getsizeof(self._cache)))

    def persist(self):
        with open(self._cache_path, 'wb') as f:
            pickle.dump(self._cache, f, pickle.HIGHEST_PROTOCOL)

    def cache(self, key: str, value: object):
        """
        None values are considered as invalid results (ToughRequest) is producing none for exceptions
        set -1 if you want to store "No distance"
        :param key:
        :param value:
        :return:
        """
        self._lock.acquire()
        if value is not None:
            self._cache[key] = self._pack(value);
            self.log.debug(self._cache_path + ' CACHED: ' + str(key) + ': ' + str(value))
            self.persist()
        self._lock.release()

    def get(self, key):
        """
        Read cache entries
        :param key:
        :return:
        """
        self._lock.acquire()
        result = None
        value = self._cache.get(key)
        if value is not None:
            self.log.debug(self._cache_path + ' LOADED: ' + str(key) + ': ' + str(value))
            result = self._unpack(value)

        self._lock.release()
        return result

    def get_complex(self, list_of_keys: List[str]):
        """
        Read complex cache entries
        """
        return self.get(self._get_id(list_of_keys))

    def cache_complex(self, list_of_keys: List[str], value):
        """
        helper to cache multi (string)key values.
        They are sorted before concatenation, therefore an order is determined.
        """
        self.cache(self._get_id(list_of_keys), value)

    def _get_id(self, list_of_keys: List[str]):
        """
        sorts list_of_keys, concatenates with # for readability
        :param list_of_keys:
        :return:
        """
        sorted(list_of_keys)
        return "#".join(list_of_keys)

    def _pack(self, value):
        """
        cache tracks the age of an entry, may be helpful in the future
        :param value:
        :return:
        """
        return [value, str(time.time())]

    def _unpack(self, value):
        """
        removes the timestamp around the cached value, if any
        :param value:
        :return:
        """
        # there are some old entries without timestamp
        if isinstance(value, str) or isinstance(value, int):
            return value
        return value[0]
