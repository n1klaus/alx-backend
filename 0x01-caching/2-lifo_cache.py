#!/usr/bin/env python3
"""LIFO Cache Replacement System"""

from base_caching import BaseCaching
from typing import Any


class SinglyLinkedNode:
    """Class to define singly linked node"""

    def __init__(self, key: Any, item: Any, next: Any):
        """Instantiates Node objects"""
        self.key: Any = key
        self.item: Any = item
        self.next: SinglyLinkedNode = next


class Stack:
    """Class to define LIFO order Stack structure"""

    def __init__(self):
        """Instantiates Stack objects"""
        self.top: SinglyLinkedNode = None

    def isEmpty(self) -> bool:
        """Checks if the stack is empty"""
        return self.top is None

    def peek(self) -> Any:
        """Returns the item at the top of the stack"""
        return self.top.key if not self.isEmpty() else None

    def push(self, key, value) -> SinglyLinkedNode:
        """Adds an item at the end(top) of the stack"""
        node: SinglyLinkedNode = SinglyLinkedNode(key, value, None)

        if self.top is not None:
            node.next = self.top
        self.top = node
        return node

    def pop(self) -> Any:
        """Removes the last(top) item in the stack"""
        if not self.isEmpty():
            key = self.top.key
            self.top = self.top.next
        return key


class LIFOCache(BaseCaching):
    """Class to define LIFO cache replacement algorithm"""

    def __init__(self, *args, **kwargs):
        """Instantiates new objects"""
        super().__init__(*args, **kwargs)
        self._queue = Stack()

    def put(self, key: Any, item: Any) -> None:
        """Inserts item into cache"""
        if key and item is not None:
            if key not in self.cache_data and \
                    len(self.cache_data.keys()) >= self.MAX_ITEMS:
                discarded_key: Any = self._queue.pop()
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")
            node: SinglyLinkedNode = self._queue.push(key, item)
            self.cache_data[key] = item

    def get(self, key: Any) -> Any:
        """Returns item from cache using provided key"""
        return self.cache_data.get(key, None)
