#!/usr/bin/env python3
"""LRU Cache Replacement System"""

from base_caching import BaseCaching
from typing import Any


class LFUCache(BaseCaching):
    """Class to define LFU cache replacement algorithm"""

    def __init__(self, *args, **kwargs):
        """Instantiates new objects"""
        super().__init__(*args, **kwargs)
        self._counter = []
        self._items = {}

    def put(self, key: Any, item: Any) -> None:
        """Inserts/Updates item in cache"""
        if key and item is not None:
            if key not in self.cache_data and\
                    len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = min(self._items.values())
                least_frequents = []
                for k, v in self._items.items():
                    if v == discarded_key:
                        least_frequents.append(k)
                if len(least_frequents) > 1:
                    saved = {}
                    for k in least_frequents:
                        saved[k] = self._counter.index(k)
                    discard = min(saved.values())
                    discard = self._counter[discard]
                else:
                    discard = least_frequents[0]
                print("DISCARD: {}".format(discard))
                del self.cache_data[discard]
                del self._counter[self._counter.index(discard)]
                del self._items[discard]
            if key in self._items:
                self._items[key] += 1
            else:
                self._items[key] = 1
            if key in self._counter:
                del self._counter[self._counter.index(key)]
            self._counter.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Updates access counter record for frequently used
        and returns the item from cache using provided key
        """
        if key is not None and key in self.cache_data.keys():
            del self._counter[self._counter.index(key)]
            self._counter.append(key)
            self._items[key] += 1
            return self.cache_data.get(key)
        return None
