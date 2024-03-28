from __future__ import annotations
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *
from algorithms.binary_search import binary_search
from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Initialised mountain_obj list

        Args:
        - None

        Raises:
        -None

        Returns:
        -None

        Complexity:
        -Worst Case: O(1), constant
        -Best Case: O(1), constant
        -Explantion: creating an empty list is O(1)
        """
        self.mountain_obj = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        By using binary search to search the current rank of the given mountain
        if mountain not exist then raise error

        Args:
        - mountain representing Mountain object

        Raises:
        -KeyError if mountain not exist

        Returns:
        -Integer representing the rank of the mountain

        Complexity:
        -Worst Case: O(log n), where n is the length of the mountain list
        -Best Case: O(log n), where n is the length of the mountain list
        -Explantion: binary search is O(log n) where n is the length of the mountain list and the rest are O(1)
        """
        position = binary_search(self.mountain_obj, mountain)
        if mountain not in self.mountain_obj:
            raise KeyError("Mountain not exist")
        return position

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        add mountain to the mountain list and sort by length and if they have the same length
        sort by lexicography order

        Args:
        -mountain representing list of mountain

        Raises:
        -None

        Returns:
        -None

        Complexity:
        -Worst Case: O(mlogm + n),M is the length of the input list to the mergesort algorithm, and N is the total number of mountains included so far.
        -Best Case: O(mlogm + n), M is the length of the input list to the mergesort algorithm, and N is the total number of mountains included so far.
        -Explantion: merge sort is O(mlogm) and appending mountain into self.mountain_obj is O(n)
        """
        for i in mountains:
            self.mountain_obj.append(i)
        self.mountain_obj = mergesort(self.mountain_obj)












