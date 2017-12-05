import threading

from tools.key_value_cache import KeyValueCache


class CacheManager:
    """
    helper to create per cache file just one instance
    """

    # singleton reference pointer
    __manager = None

    def __init__(self):
        self._instances = {}
        self._lock = threading.Lock()

    def get_cache(self, path):
        """
        :param path: path to cache, relative to root.py
        :return:
        """
        self._lock.acquire()
        instance = self._instances.get(path)
        if instance is None:
            instance = KeyValueCache(path)
            self._instances[path] = instance
        self._lock.release()
        return instance

    def persist(self):
        """
        persist all alive cache objects
        :return:
        """
        self._lock.acquire()
        for instance in self._instances:
            self._instances[instance].persist()
        self._lock.release()

    @classmethod
    def instance(cls):
        """
        return the cache manager instance
        :return:
        """
        if cls.__manager is None:
            cls.__manager = CacheManager()
        return cls.__manager;
