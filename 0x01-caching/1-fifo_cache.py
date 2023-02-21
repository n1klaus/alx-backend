#!/usr/bin/env python3
"""FIFO Cache Replacement System"""

from base_caching import BaseCaching
from typing import Any


class DoublyLinkedNode:
    """Class to define doubly linked node"""

    def __init__(self, prev: Any, key: Any, item: Any, next: Any):
        """Instantiates Node objects"""
        self.prev: DoublyLinkedNode = prev
        self.key: Any = key
        self.item: Any = item
        self.next: DoublyLinkedNode = next


class Queue:
    """Class to define FIFO order Queue structure"""

    def __init__(self):
        """Instantiates Queue objects"""
        self.front: DoublyLinkedNode = None
        self.rear: DoublyLinkedNode = None

    def isEmpty(self) -> bool:
        """Checks if the queue is empty"""
        return self.front is None

    def append(self, key, value) -> DoublyLinkedNode:
        """Adds an item at the end of the queue"""
        node: DoublyLinkedNode = DoublyLinkedNode(None, key, value, None)

        if self.front is None:
            self.front = node
        else:
            self.rear.next = node
            node.prev = self.rear
        self.rear = node
        return node

    def popleft(self) -> Any:
        """Removes the first item in the queue"""
        if not self.isEmpty():
            key = self.front.key
            self.front = self.front.next
            if self.front is not None:
                self.front.prev = None
        return key


class FIFOCache(BaseCaching):
    """Class to define FIFO cache replacement algorithm"""

    def __init__(self, *args, **kwargs):
        """Instantiates new objects"""
        super().__init__(*args, **kwargs)
        self._queue = Queue()

    def put(self, key: Any, item: Any) -> None:
        """Inserts item into cache"""
        if key and item is not None:
            if len(self.cache_data.keys()) >= self.MAX_ITEMS:
                discarded_key: Any = self._queue.popleft()
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")
            node: DoublyLinkedNode = self._queue.append(key, item)
            self.cache_data[key] = item

    def get(self, key: Any) -> Any:
        """Returns item from cache using provided key"""
        return self.cache_data.get(key, None)
