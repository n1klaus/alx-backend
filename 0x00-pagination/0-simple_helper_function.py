#!/usr/bin/env python3
"""Simple pagination helper function"""

from typing import Tuple


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
