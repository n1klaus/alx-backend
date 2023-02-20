#!/usr/bin/env python3

import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Args:
        page (int): selected page
        page_size (int): set page size
    Returns:
        a tuple containing the start index and end index for a page
    """
    start_index: int = 0 if page == 1 else (page - 1) * page_size
    end_index: int = page_size if page == 1 else page * page_size
    return (start_index, end_index)


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    @property
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

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Args:
            page (int): selected page
            page_size (int): set page size
        Returns:
            the appropriate page with correct indexes to paginate the dataset
        """
        assert isinstance(page and page_size, int)
        assert page > 0 and page_size > 0

        return_page: list = []
        start_index, end_index = index_range(page, page_size)
        if self.dataset and len(self.dataset) > end_index:
            return_page = self.dataset[start_index: end_index]
        return return_page
