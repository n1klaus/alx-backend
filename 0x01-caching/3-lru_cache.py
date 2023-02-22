#!/usr/bin/env python3
"""LRU Cache Replacement System"""

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


class LRUReverseQueue:
    """Class to define LRU order ReverseQueue structure"""

    def __init__(self):
        """Instantiates ReverseQueue objects"""
        self.head: DoublyLinkedNode = None
        self.tail: DoublyLinkedNode = None

    def isEmpty(self) -> bool:
        """Checks if the queue is empty"""
        return self.head is None

    def find(self, key: Any) -> DoublyLinkedNode:
        """Returns node with the known key"""
        if self.isEmpty():
            return None

        node: DoublyLinkedNode = self.head
        # Iterate the queue to find a match
        while node is not None:
            # If it is a positive match return
            if node.key == key:
                return node
            node = node.next

        return None

    def get(self, key: Any) -> DoublyLinkedNode:
        """Gets the node with the key and updates it
        as recently used by moving it to the head"""
        node: DoublyLinkedNode = self.find(key)

        if node is not None:
            # If it is already at the front leave it
            if node is self.head:
                pass
            else:
                # If it is at the rear
                if node is self.tail:
                    self.tail = node.prev

                # Update its position to the front and
                # connect its neighbouring nodes
                if node.next is not None:
                    node.next.prev = node.prev
                if node.prev is not None:
                    node.prev.next = node.next

                self.head.prev = node
                node.next = self.head
                node.prev = None
                self.head = node
        return node

    def insert(self, key, value) -> DoublyLinkedNode:
        """Adds/Updates a node in the queue"""
        # First check if node already exists
        node: DoublyLinkedNode = self.get(key)
        if node is not None:
            # Update the value stored for the existing node
            node.item = value
            return node
        else:
            # Create a new node if it doesn't exist
            node: DoublyLinkedNode = DoublyLinkedNode(None, key, value, None)

        # Insert in front
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        return node

    def remove(self) -> Any:
        """Removes the least recently used(last) item in the queue"""
        if not self.isEmpty():
            key = self.tail.key
            self.tail = self.tail.prev
            if self.tail is not None:
                self.tail.next = None
        return key

    def __str__(self):
        """Overrides and returns string representation of instance"""
        my_list: list = []
        temp: DoublyLinkedNode = self.head

        if not self.isEmpty():
            while temp is not None:
                my_list.append(f"({temp.key}, {temp.item})")
                temp = temp.next
        return ", ".join(my_list)


class LRUCache(BaseCaching):
    """Class to define LRU cache replacement algorithm"""

    def __init__(self, *args, **kwargs):
        """Instantiates new objects"""
        super().__init__(*args, **kwargs)
        self._queue = LRUReverseQueue()

    def put(self, key: Any, item: Any) -> None:
        """Inserts/Updates item in cache"""
        if key and item is not None:
            if key not in self.cache_data and \
                    len(self.cache_data.keys()) >= self.MAX_ITEMS:
                discarded_key: Any = self._queue.remove()
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")
            node: DoublyLinkedNode = self._queue.insert(key, item)
            self.cache_data[key] = item

    def get(self, key: Any) -> Any:
        """
        Updates access record as recently used
        and returns the item from cache using provided key
        """
        node: DoublyLinkedNode = self._queue.get(key)
        return self.cache_data.get(key, None)
