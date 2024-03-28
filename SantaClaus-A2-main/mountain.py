from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __le__(self, other: Mountain)-> bool:
        """
        A magic method for comparing, when mountain compares with other mountain it compares in terms of the length when
        mountain length is less or equal than the other one then return True. If is same then use lexicography order. Else return
        False

        Args:
        - other representing other Mountain object

        Raises:
        -None

        Returns:
        -Boolean representing more or less than

        Complexity:
        -Worst Case: O(1*comp), comp representing complexity
        -Best Case: O(1*comp), comp representing complexity
        -Explantion: all is constant
        """
        if self.length <= other.length:
            return True
        elif self.length == other.length:
            return self.name <= other.name
        else:
            return False

    def __gt__(self, other:Mountain)-> bool:
        """
        A magic method for comparing, when mountain compares with other mountain it compares in terms of the length when
        mountain length is greater than the other one then return True. If is same then use lexicography order. Else return
        False

        Args:
        - other representing other Mountain object

        Raises:
        -None

        Returns:
        -Boolean representing more or less than

        Complexity:
        -Worst Case: O(1*comp), comp representing complexity
        -Best Case: O(1*comp), comp representing complexity
        -Explantion: all is constant
        """
        if self.length > other.length:
            return True
        elif self.length == other.length:
            return self.name > other.name
        else:
            return False
