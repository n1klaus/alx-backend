#!/usr/bin/env python3
"""Basic Caching System"""

from base_caching import BaseCaching
from typing import Any


class BasicCache(BaseCaching):
    """Class to define basic caching system"""

    MAX_ITEMS = None

    def __init__(self, *args, **kwargs):
        """Instantiates new objects"""
        super().__init__(*args, **kwargs)

    def put(self, key: Any, item: Any) -> None:
        """Inserts item into cache"""
        if key and item is not None:
            self.cache_data[key] = item

    def get(self, key: Any) -> Any:
        """Returns item from cache using provided key"""
        return self.cache_data.get(key, None)
