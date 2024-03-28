from mountain import Mountain
from algorithms.mergesort import mergesort
from double_key_table import DoubleKeyTable


class MountainManager:
    """
    MountainManager acts as a store which tracks all mountains in a trail
    and can be used to edit, add or remove mountains.

    Implemented using ADT DoubleKeyTable.

    K1: str(mountain.difficulty_level), allows grouping by difficulty in top table
    K2: mountain.name

    """

    def __init__(self) -> None:
        """
        Initialization of the object.

        Complexity:
        Best and worst case both O(n), n is the table size of DoubleKeyTable.
        An underlying array for DoubleKeyTable is created every time an object of it is instantiated.
        """
        self.mountain = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Adding a mountain to MountainManager.

        Arguments:
            - mountain: instance of Mountain to be added to the store

        Complexity:
        Best and worst case both O(1),
        where we assume adding a mountain into the hash table is O(1).
        """
        self.mountain[str(mountain.difficulty_level), str(mountain.name)] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Deleting a mountain from MountainManager.

        Arguments:
            - mountain: instance of Mountain to be deleted from the store

        Complexity:
        Best and worst case both O(1),
        where we assume deleting a mountain from the hash table is O(1).
        """
        del self.mountain[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Remove the old mountain and add the new mountain.

        Arguments:
            - mountain: instance of Mountain to be deleted from the store

        Complexity:
        Best and worst case both O(1),
        where we assume deleting/adding a mountain from the hash table is O(1).
        """
        del self.mountain[str(old.difficulty_level), old.name]
        self.mountain[str(new.difficulty_level), new.name] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Return a list of all mountains with this difficulty.

        Arguments:
            - diff: Difficulty level

        Complexity:
        Best and worst case both O(n),
        where n is the size of the number of mountains with the difficulty level stated.
        """
        mountain_diff = []
        try:
            self.mountain.values(str(diff))
        except KeyError:
            return mountain_diff
        else:
            for item in self.mountain.iter_values(str(diff)):
                mountain_diff.append(item)
        return mountain_diff

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.

        Complexity:
        Best and worst case both O(n*log(n) + k*n), where n is the size of the number of mountains with the difficulty
        level stated and k is the number of different difficulty levels in the hash table.
        get_difficulty is O(n*log(n)), followed by the loop with a call of mountains_with_difficulty that has
        O(n) complexity gives overall O(k*n).
        """
        mountain_sort_diff = []
        for i in self.get_difficulty():
            mountain = self.mountains_with_difficulty(i)
            if len(mountain) != 0:
                mountain_sort_diff.append(mountain)
        return mountain_sort_diff

    def get_difficulty(self) -> list[int]:
        """
        Returns a list of all integer values of difficulty levels (sorted) in a list.

        Complexity:
        Best and worst case both O(n*log(n)), where n is the number of top-level keys (difficulty
        levels of all mountains in the MountainManager). The for loop has complexity O(n) and
        mergesort has a complexity of O(n*log(n)).O(n + n*log(n)) = O(n*log(n)).
        """
        ret = []
        for diff_lvl in self.mountain.iter_keys():
            if int(diff_lvl) not in ret:
                ret.append(int(diff_lvl))
        ret = mergesort(ret)
        return ret

