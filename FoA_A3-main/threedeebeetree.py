from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field
from referential_array import ArrayR

I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:

    key: Point
    item: I
    subtree_size: int = 1
    children: list[BeeNode] = field(default_factory=list)
    binary_lst: list[str] = field(default_factory=list)

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        """
        complexity:
        Best case  = Worst Case: O(1) * O(comp),where O(comp) is the comparison's complexity get_octant is O(1) and everything is O(1)

        Best case same as worst case because they need to experience the same process no matter what
        """
        octant_index = self.get_octant(point) #O(1)
        if octant_index is not None:
            try:
                node = self.children[octant_index]
                return node
            except IndexError:
                return None

    def set_child_for_key(self, key, item):
        """
        complexity:
        Best case = Worst Case: O(1) * O(comp),where O(comp) is the comparison's complexity get_octant is O(1) and everything is O(1)

        Best case same as worst case because they need to experience the same process no matter what
        """
        self.subtree_size += 1
        new_node = BeeNode(key, item)
        node = self.get_child_for_key(key)
        octant_index = self.get_octant(key)
        if node is None:
            self.children.insert(octant_index, new_node)
            return True

    def get_octant(self, key):
        """
        complexity:
        Best case = Worst case: O(1) * O(comp), where comp is comparison complexity
                                the length of key is always 3. So is O(1). and the rest is O(1) as well
                                so overall the complexity is O(1) * O(comp)

        Best case same as worst case because they need to experience the same process no matter what
        """
        octant = ''
        for i in range(len(key)): #constant 3
            if key[i] >= self.key[i]:
                octant += "1"
            else:
                octant += "0"

        if octant not in self.binary_lst: #O(comp)
            self.binary_lst.append(octant)

        octant_index = self.binary_lst.index(octant)
        return octant_index


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0
        self.binary_lst = []
        self.node_lst = []

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        """
        Complexity:
        Best case: O(1) * O(comp), when the root is the key. No need further traverse so is O(1)
        Worst case: O(log n) * O(comp), where n is the number of nodes in the tree, comp is comparison complexity
                    when the key is the leaf node. Makes it keep traversing through the subtree until the leaf node.
                    so it depends on the depth, which is log n in a balanced tree
        """
        if self.root.key == key:
            return self.root
        else:
            flag = True
            octant_index = self.root.get_octant(key) #O(1)
            node = self.root.children[octant_index]
            while flag: #O(
                if node.key == key:
                    return node
                elif self.is_leaf(node):
                    flag = False
                    return None
                else:
                    octant_index = node.get_octant(key)
                    node = node.children[octant_index]

    def __setitem__(self, key: Point, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)
        self.length += 1

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            complexity:

            Balance tree
            Best case = Worst Case: O(log n) * O(comp), where n is the number of nodes in the tree, comp is comparison complexity
                                    assuming the tree is balance, it needs to traverse and compare based on the octant and insert
                                    so it depends on the depth of the tree which is log n.

            In balance tree best case = worst case as they need to traverse through the node based on the octant no matter what

            unbalance tree
            Best case: O(1) * O(comp), comp is comparison complexity
                             when the root only has one octant occupied and the others were empty. Being insert into other octant of
                             the root. so is O(1) as it does not need to traverse down the tree.

            Worst case: O(n) * O(comp), where n is the number of nodes in the tree, comp is comparison complexity
                              when all node in one octant and all the node has the same symbol, which formed a line all the way
                              down. So when it inserts the same symbol node. It needs to traverse all the way down to the bottom
                              to insert. So is O(n)
        """
        if current is None:
            new_node = BeeNode(key, item)
            self.node_lst.append(new_node)
            return new_node

        node = current.set_child_for_key(key,item)
        if node:
            return self.root
        else:
            child = current.get_child_for_key(key)
            self.insert_aux(child, key, item)

        return self.root


    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """
        return current.subtree_size == 1

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"

    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2




