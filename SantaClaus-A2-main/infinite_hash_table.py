from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int | None = 0) -> None:
        """
        Initialization of object.

        Arguments:
            - level: level of the hash table

        Complexity:
        Best and worst case both O(n), where n is the table size.
        As an array object with n slots is initialized each time.
        """
        self.level = level
        if self.level == 0:
            self.HEAD = self
        self.count = 0
        self.array: ArrayR[InfiniteHashTable] = ArrayR(self.TABLE_SIZE)

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Arguments:
            - key: key of the element to be retrieved

        Complexity:
        Let comparison be O(comp).
        Best case: O(comp), when the item is at the position in the level 0 table.
        Worst case: O(n*comp), where n is the number of levels to get to the item, when the item is at the last level table.
        """
        if self.level == 0:
            self.get_location(key)
        pos = self.hash(key)
        if isinstance(self.array[pos], InfiniteHashTable):
            ret = self.array[pos]
        if type(self.array[pos]) is tuple:
            ret = self.array[pos][1]
        return ret

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set a (key, value) pair in our hash table.

        Arguments:
            - key: key of the element to be added

        Complexity:
        Let comparison be O(comp),
        d is depth of the tables (number of levels).
        Best case: O(comp), when the item can be directly inserted into the level 0 table.
        Worst case: O(comp*d), when the item needs to be inserted at the kth level hash table.
        """
        pos = self.hash(key)

        if self.array[pos] is None:
            self.array[pos] = (key, value)
            self.count += 1
        elif type(self.array[pos]) is tuple and self.array[pos][0] == key:
            self.array[pos] = (key, value)
        else:
            temp = self.array[pos]
            if type(temp) is not InfiniteHashTable:
                self.array[pos] = InfiniteHashTable((self.level + 1))
                self.array[pos][temp[0]] = temp[1]
                self.count -= 1
            
            self.array[pos][key] = value


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Arguments:
            - key: key of the element to be deleted

        Complexity:
        n is size of the hash table,
        k is depth of the hash table (number of levels).
        Best case: O(k),
        when the item is at the kth sub-table and all sub-tables in the hash table have more than 1 valid elements
        (no rehashing).
        Worst case: O(n*k + n^2),
        when the item is at the kth sub-table and all of the levels have 1 or less valid elements and references.
        """
        if self.level == 0:
            self.get_location(key)
        pos = self.hash(key)
        if isinstance(self.array[pos], InfiniteHashTable):
            del self.array[pos][key]
        else:
            if self.array[pos][0] == key:
                self.array[pos] = None
                self.count -= 1
        self.check_hashtable(pos)

    def check_hashtable(self, pos: int, flag: bool = True, item: tuple = None, item_pos: int = None) -> None:
        """
        Checks if only a single pair/no pair within the table in a specific slot,
        with the table no references to other hash tables,
        if there is only a single pair, the table is collapsed to a single entry in the parent table.
        if there is no pair, the current table is deleted in the parent table.

        Arguments:
            - pos: position of the array that is checked
            (The three below are meant to be used as defaults)
            - flag: boolean value to check if the table in the specific slot has instances of InfiniteHashTable
            - item: stores the key, value pair to be rehashed if it is the only element in the table
            - item_pos: stores the position of the key, value pair in the table of a specific slot

        Complexity:
        Best case: O(n), where n is size of the hash table,
        when all sub-tables in the hash table have more than 1 valid elements.
        Worst case: O(n^2), where n is size of the hash table,
        when all sub-tables in the hash table has 1 valid element or less.
        """
        if isinstance(self.array[pos], InfiniteHashTable):
            for index in range(len(self.array[pos].array)):
                if isinstance(self.array[pos].array[index], InfiniteHashTable):
                    flag = False
                if isinstance(self.array[pos].array[index], tuple):
                    item_pos = index
                    item = self.array[pos].array[index]
            if len(self.array[pos]) == 0 and flag:
                self.array[pos] = None
            elif len(self.array[pos]) == 1 and flag:
                self.array[pos].array[item_pos] = None
                self.array[pos].count -= 1
                self.array[pos] = None
                self[item[0]] = item[1]

    def __len__(self):
        """
        Returns the number of elements currently in the hash table.

        Complexity:
        n is the size of the underlying array,
        d is the number of levels in the array,
        O(comp) is the complexity of comparison.

        Best case: O(n*comp), when calling the function at the last level of the hash table with no references
        to other levels.

        Worst case: O(n*k*comp), when calling the function at the level 0 of the hash table and going through
        all levels at each position of the array.
        """
        count = self.count
        for index in range(len(self.array)):
            if type(self.array[index]) is InfiniteHashTable:
                count += len(self.array[index])
        return count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Arguments:
            - key: key of the element to find

        Complexity:
        Let comparison be O(comp).
        Best case: O(comp), when the item is at the position in the level 0 table.
        Worst case: O(n*comp), where n is the number of levels to get to the item, when the item is at the last level table.
        """
        pos = self.hash(key)
        if self.array[pos] is not None:
            if type(self.array[pos]) is tuple and self.array[pos][0] == key:
                return [pos]
            elif type(self.array[pos]) is InfiniteHashTable:
                return [pos] + self.array[pos].get_location(key)
            else:
                raise KeyError("Key doesn't exist.")
        raise KeyError("Key doesn't exist.")

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

