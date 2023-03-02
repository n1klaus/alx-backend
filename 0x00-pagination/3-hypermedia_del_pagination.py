#!/usr/bin/env python3
"""
Deletion-resilient hypermedia seek pagination
"""

import csv
import math
from typing import Any, Dict, List


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: d for i, d in enumerate(dataset)
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict[str, Any]:
        """
        Args:
            index (int): the index of the first item in the current page
            page_size (int): the length of the returned dataset page
        Returns:
            the appropriate page information
        """
        assert isinstance(index and page_size, int)
        dataset: dict = self.dataset()
        indexed_dataset: dict = self.indexed_dataset()
        assert 0 <= index < len(indexed_dataset) and page_size > 0

        
        PAGE_FIX: bool = False
        for i in range (index, len(indexed_dataset.keys())):
            if i not in indexed_dataset.keys() or PAGE_FIX:
                next_data_index: int = i + 1
                while True:
                    data: Any = indexed_dataset.get(next_data_index)
                    if data is not None:
                        break
                    next_data_index += 1
                indexed_dataset[index] = data
                PAGE_FIX = True

        next_index: int = index + page_size
        data: List[str] = [
            d for d in list(indexed_dataset.values())[index: next_index]
        ]

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index
        }
