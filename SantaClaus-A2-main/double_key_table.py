from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Initialization.
        
        Type Arguments:
        - sizes representing a list of table sizes
        - internal_sizes representing size of inner array

        Complexity:
        Best and worst case both O(n), where n is the size of the outer table.
        As an underlying array of table size is created.
        
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array = ArrayR(self.TABLE_SIZES[0])
        self.count = 0
        self.top_table_length = 0
        self.internal_sizes = None
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def create_low_level_table(self) -> LinearProbeTable:
        """
        Creates the internal hash table object.

        Complexity:
        Best and worst case both O(n), where n is the size of the internal table.
        As a LinearProbeTable with underlying array of table size is created.

        """
        table = LinearProbeTable(self.internal_sizes)
        table.hash = lambda k: self.hash2(k, table)
        return table

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct postion for this key in the hash table using linear probing

        Type Arguments:
        - key1 representing K1 object
        - key2 representing K2 object
        - is_insert representing a boolean where it indicates inserting value to the hash table or no

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Complexity:
        Let comparison be O(comp).
        Best case: O(len(key)), when the correct position is found at once in the hashed position,
        using probe_top_table and probing through the internal table.
        Worst case: O(len(key) + n*comp), where n is max(size_top_table, size_internal_table), where both tables
        have been searched through fully.

        """
        pos_top = self.probe_top_table(key1, is_insert)
        pos_low = self.array[pos_top][1]._linear_probe(key2, is_insert)
        return (pos_top, pos_low)

    def probe_top_table(self, key1: K1, is_insert: bool) -> int:
        """
        Probe through top table to get the position index.
        Creates an internal hash table if is_insert.
        
        Type Arguments:
        - key1 representing K1 object
        - is_insert representing a boolean where it indicates inserting value to the hash table or no

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Return:
        -position indicates the position of the hash table

        Complexity:
        Let comparison be O(comp).
        Best case: O(len(key)+comp), when the item is found at the hashed position of table at once, with no probing needed.
        Worst case: O(n*comp), where n is the size of the table, when we want insert a key and the hash table is full.

        """
        position = self.hash1(key1)
        for _ in range(self.table_size):
            if self.array[position] is None:
                if is_insert:
                    self.array[position] = (key1, self.create_low_level_table())
                    self.top_table_length += 1
                    return position
                else:
                    raise KeyError(key1)
            elif self.array[position][0] == key1:
                return position
            else:
                position = (position + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key1)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity:
        Best case: O(1), when the key is None and we want to return an iterator of all top_level keys.
        Worst case: O(n), where n is the size of the outer table,
        when the key is stated, so we need to probe through the top table to get the position of the key.
        """
        if key is None:
            return KeyValueIterator(self, 0)
        else:
            pos = self.probe_top_table(key, False)
            sub_table = self.array[pos][1]
            return KeyValueIterator(sub_table, 0)


    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        
        Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.

        Return:
        - ret representing a list of keys in the hash table
        
        Complexity:
        Best and worst case both O(n), where n is the size of the number of keys in the table/top_level key x.
       
        """
        ret = []
        if key is None:
            for item in self.iter_keys():
                ret.append(item)
        else:
            for item in self.iter_keys(key):
                ret.append(item)
        return ret

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Complexity:
        Best case: O(1), when the key is None and we want to return an iterator of all values in the hash table.
        Worst case: O(n), where n is the size of the outer table,
        when the key is stated, so we need to probe through the top table to get the position of the key.
        """
        if key is None:
            return FullValueIterator(self)
        else:
            pos = self.probe_top_table(key, False)
            sub_table = self.array[pos][1]
            return KeyValueIterator(sub_table, 1)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.

        Return:
        -ret representing a list of values of the keys
        
        Complexity:
        Best and worst case both O(n), where n is the size of the number of values in the table/top_level key x.
        """
        ret = []
        if key is None:
            for item in self.iter_values():
                ret.append(item)
        else:
            for item in self.iter_values(key):
                ret.append(item)
        return ret
      
    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        Type Arguments:
        - key represents a tuple of keys

        :raises KeyError: when the key doesn't exist.
        
        Return:
        - The value at certain key

        Complexity:
        Let comparison be O(comp).
        Best case: O(len(key)), when the item is found at the first position searched in both top/bottom tables.
        Worst case: O(len(key) + n*comp), where n is table size, when we've searched the entire table.
        """
        key1, key2 = key
        pos_top, pos_low = self._linear_probe(key1, key2, False)
        return self.array[pos_top][1][pos_low]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        
        Type Arguments:
        - key represents a tuple of keys
        - data represents a value

        Complexity:
        Let comparison be O(comp).
        Best case: O(len(key)), when the item is can be at the first position hashed to in both top/bottom tables.
        Worst case: O(len(key) + n*comp), where n is table size, when we've searched the entire table for an empty slot.
        """
        key1, key2 = key
        pos_top, pos_low = self._linear_probe(key1, key2, True)

        sub_table = self.array[pos_top][1]
        if sub_table.array[pos_low] is None:
            self.count += 1

        sub_table[key2] = data

        if self.top_table_length > self.table_size / 2:
            print(len(self))
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Type Arguments:
        - key represents a tuple of keys

        :raises KeyError: when the key doesn't exist.

        Complexity:
        Let comparison be O(comp).
        Best case: O(len(key)), when the item is found at the first position searched in both top/bottom tables.
        Worst case: O(len(key) + n*comp), where n is table size, when we've searched the entire table.
        """
        key1, key2 = key
        pos_top, pos_low = self._linear_probe(key1, key2, False)
        # Remove the element
        sub_table = self.array[pos_top][1]
        del sub_table[key2]
        self.count -= 1
        if sub_table.is_empty():
            self.array[pos_top] = None
            self.top_table_length -= 1

        # Start moving over the cluster
        pos_top = (pos_top + 1) % self.table_size
        while self.array[pos_top] is not None:
            key1, sub_table = self.array[pos_top]
            self.array[pos_top] = None
            # Reinsert.
            newpos = self.probe_top_table(key1, True)
            self.array[newpos] = (key1, sub_table)
            pos_top = (pos_top + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Type Arguments:
        -None

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index == len(self.TABLE_SIZES):
            return None
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None:
                key1, sub_table = item
                pos = self.probe_top_table(key1, True)
                self.array[pos] = item

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        Complexity:
        O(1)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Complexity:
        O(1)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

class KeyValueIterator:
    """
    used for:
    keys(outer/inner) and values of specific key.
    only works with one specific hash table
    indicator: int 0 for key and 1 for value
    """
    def __init__(self, hash_table: DoubleKeyTable|LinearProbeTable, indicator: int) -> None:
        """
        Complexity:
        O(1)
        """
        self.table = hash_table
        self.indicator = indicator
        self.index_tracker = 0

    def __iter__(self) -> Iterator[K1]:
        """
        Complexity:
        O(1)
        """
        return self

    def __next__(self) -> K1:
        """
        Complexity:
        Let comparison be O(comp).
        Best and worst case both O(comp).
        """
        while self.index_tracker < self.table.table_size:
            if self.table.array[self.index_tracker] is not None:
                ret = self.table.array[self.index_tracker][self.indicator]
                self.index_tracker += 1
                return ret
            self.index_tracker += 1
        raise StopIteration

class FullValueIterator:
    """
    Iterator for values of the full hash table (all inner tables)
    """
    def __init__(self, hash_table: DoubleKeyTable) -> None:
        """
        Complexity:
        O(1)
        """
        self.table = hash_table
        self.current = None
        self.index_tracker = 0

    def __iter__(self) -> Iterator[V]:
        """
        Complexity:
        O(1)
        """
        return self

    def __next__(self) -> K1:
        """
        Complexity:
        Let comparison be O(comp).
        Best and worst case both O(comp).
        """
        while self.index_tracker < self.table.table_size:
            if self.table.array[self.index_tracker] is not None:
                sub_table = self.table.array[self.index_tracker][1]
                if self.current is None:
                    self.current = KeyValueIterator(sub_table, 1)
                try:
                    ret = next(self.current)
                except StopIteration:
                    self.current = None
                else:
                    return ret

            self.index_tracker += 1
        raise StopIteration

# if __name__ == '__main__':
#     dt = DoubleKeyTable()
#     dt["May", "Jim"] = 1
#     dt["Kim", "Tim"] = 2
#     dt["May", "Ana"] = 4
#
#     key_iterator = dt.iter_keys()
#     key2_iterator = dt.iter_keys("May")
#     value_iterator = dt.iter_values()
#
#     # key = next(key_iterator)
#     # print(key)
#     # key = next(key_iterator)
#     # print(key)
#     # key = next(key2_iterator)
#     # print(key)
#     # key = next(key2_iterator)
#     # print(key)
#     value = next(value_iterator)
#     print(value)
#     value = next(value_iterator)
#     print(value)
#     value = next(value_iterator)
#     print(value)
#     value = next(value_iterator)
#     print(value)

