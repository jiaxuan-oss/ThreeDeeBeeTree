from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil, floor
from bst import BinarySearchTree
from node import TreeNode

T = TypeVar("T")
I = TypeVar("I")


class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        Complexity:
        Best = worst case: O(1), creating a BST.
        """
        self.bst = BinarySearchTree()

    
    def add_point(self, item: T) -> None:
        """
        Complexity:
        (Dependent on complexity of add in BST)

        Let n be the number of elements in the BST.
        O(comp) is complexity of comparison.
        Best case: O(1)*O(comp), when the BST is highly unbalanced,
        all elements in the BST skew to the left, and the element to be added is
        larger than all elements in the BST (add to the right).

        Worst case: O(n)*O(comp), when the BST is highly unbalanced,
        all elements in the BST skew to the left, and the element to be added is
        smaller than all elements in the BST, which needs to traverse the BST, taking O(n) complexity.
        """
        self.bst[item] = item
    
    def remove_point(self, item: T) -> None:
        """
        Complexity:
        (Dependent on complexity of delete in BST)

        Let n be the number of elements in the BST.
        O(comp) is complexity of comparison.
        Best case: O(logn)*O(comp), when the BST is balanced, only need to traverse logn depth of the BST.

        Worst case: O(n)*O(comp), when the BST is highly unbalanced,
        all elements in the BST skew to one side (left/right), and traversing the BST takes O(n) complexity.
        """

        del self.bst[item]

    def ratio(self, x, y) -> list[T]:
        """
        Complexity:
        n is the number of elements in the BST.
        O(comp) is complexity of comparison.
        Best case:
        - O(logn), complexity depends on function self.ratio_aux, other operations are either O(1) or O(1)*O(comp).

        Worst case:
        - O(n), complexity depends on function self.ratio_aux, other operations are either O(1) or O(1)*O(comp).
        """
        lower_bound_index = ceil(len(self.bst) * (x / 100))
        upper_bound_index = len(self.bst) - ceil(len(self.bst) * (y / 100)) + 1

        lower_bound = self.bst.kth_smallest(lower_bound_index, self.bst.root)
        upper_bound = self.bst.kth_smallest(upper_bound_index, self.bst.root)

        if not lower_bound:
            lower_bound = 0
        else:
            lower_bound = lower_bound.key
        if not upper_bound:
            upper_bound = (self.bst.kth_smallest(self.bst.root.subtree_size, self.bst.root)).key + 1
        else:
            upper_bound = upper_bound.key

        lst = self.ratio_aux(self.bst.root, lower_bound, upper_bound, [])
        return lst

    def ratio_aux(self, current: TreeNode, lower_bound: T, upper_bound: T, lst: list[T]) -> list[T]:
        """
        Complexity:
        n is the number of elements in the BST.
        Best case:
        - O(logn), when the BST is balanced and recursion goes on for the depth of the tree logn.

        Worst case:
        - O(n), when the BST is highly unbalanced and all elements in the BST are skewed to the left/right (no elements
        in the other side subtree)
        """
        if current is None:
            return
        else:
            if lower_bound < current.key < upper_bound:
                lst.append(current.item)
            self.ratio_aux(current.left, lower_bound, upper_bound, lst)
            self.ratio_aux(current.right, lower_bound, upper_bound, lst)

        return lst




if __name__ == "__main__":
    lst = [i for i in range(800)]
    print(lst)
    p = Percentiles()
    for i in lst:
        p.add_point(i)
    print(p.ratio(49.5, 49.5))