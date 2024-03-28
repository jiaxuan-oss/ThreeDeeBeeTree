from dataclasses import dataclass
from heap import MaxHeap


@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

    def __gt__(self, other):
        """
        complexity:
        best case = worst case: O(1), numerical comparison is O(1)
        """
        if isinstance(other, Beehive):
            return min(self.capacity, self.volume) * self.nutrient_factor > min(other.capacity, other.volume) * \
                       other.nutrient_factor

    def __le__(self, other):
        """
        complexity:
        best case = worst case: O(1), numerical comparison is O(1)
        """
        if isinstance(other, Beehive):
            return min(self.capacity, self.volume) * self.nutrient_factor <= min(other.capacity, other.volume) * \
                       other.nutrient_factor

class BeehiveSelector:

    def __init__(self, max_beehives: int) -> None:
        """
        Complexity:
        best case = worst case: O(n),
        where n is the size of max_beehives, as creating an array of len(max_beehives) is O(n) complexity

        """
        self.max_beehives = max_beehives
        self.bhs_heap: MaxHeap[Beehive] = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]) -> None:
        """
        Complexity:
        best case = worst case: O(n+m), where n is the size of self.max_beehives and m is len(hive_list).
        Creating a MaxHeap is O(n) and loop through hive_list is O(m).

        """
        temp = MaxHeap(self.max_beehives)
        for hive in hive_list:
            temp.add(hive)
        self.bhs_heap = temp

    def add_beehive(self, hive: Beehive) -> None:
        """
        Complexity:
        Best case: O(1) * O(comp), where O(comp) is the comparison complexity. When the element added is smaller than
        all the elements in the heap.

        Worst case: O(log n) * O(comp), where n is number of hive in the heap and O(comp) is the comparison complexity
        Adding an element in a heap is O(log n)*O(comp) when the element is the largest in the heap
        """
        self.bhs_heap.add(hive)

    def harvest_best_beehive(self) -> float:
        """
        Complexity:
        Best case : O(1) * O(comp), get_max best case is O(1) * O(comp) where O(comp) is comparison complexity.
        when the element in the heap are all the same. Add operation best case is O(1), and the rest all O(1). Hence
        overall complexity is O(1) * O(comp)

        Worst Case: O(log n) * O(comp), get_max worst case is O(log n) * O(comp) where n is number of hive in the heap
        and O(comp) is comparison complexity. when the element is the smallest and need to sink all the way down
        Add operation worst case is O(log n) where n is number of element in the heap and the rest all O(1).
        Hence, overall complexity is O(log n) * O(comp)
        """
        max_beehive = self.bhs_heap.get_max()
        harvest_amount = min(max_beehive.volume, max_beehive.capacity)
        max_beehive.volume -= harvest_amount
        self.bhs_heap.add(max_beehive) #O(1) best case O(Log n) worst case
        return harvest_amount * max_beehive.nutrient_factor
