""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item=item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        current.subtree_size = self.get_subtree_size(current.left) + self.get_subtree_size(current.right) + 1
        return current

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)
        current.subtree_size = self.get_subtree_size(current.left) + self.get_subtree_size(current.right) + 1
        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a child node having the smallest key among all the
            larger keys.
            Complexity:
            -Best case: O(1), when the tree is highly unbalanced, when every node is smaller than the current and only one node
                        on the right which is larger than the current. So just need to traverse once
                        which is current.right to get the successor

                        O(log n), where n is the number of node in the tree, when the tree is balanced.
                        traverse to right until it meets one left. So is depth of log n.

            -Worst Case: O(n),where n is the number of node in the tree, when the tree is highly unbalanced.
                         after one traverse to the right, and all the node is located on the left subtree,
                         so we need to traverse all the way down to the end of the left subtree. So is O(n)

                         O(log n), where n is the number of node in the tree, when the tree is balanced.
                         traverse to right until it meets one left. So is depth of log n.
        """
        if current is None or current.right is None:
            return None

        elif current.right is not None:
            current = current.right
            while current.left is not None:
                current = current.left
            return current

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree.
            complexity:
            Best case: O(1), when the tree is highly unbalanced, when every node is larger and only one node on the left side,
                             only traverse one time, so i O(1)

                        O(log n) * O(comp) where n is the number of node in the tree and comp is comparison complexity
                        when the tree is balanced and the smallest key will be at the bottom with depth of log n. Hence O(log n)*O(comp)

            worst case: O(n) * O(comp) where n is the number of node in the tree and comp is comparison complexity
                        when the tree is highly unbalanced and all element is on one side
                        need to traverse all the way down to the bottom of left subtree for the smallest key

                        O(log n) * O(comp) where n is the number of node in the tree and comp is comparison complexity
                        when the tree is balanced and the smallest key
                        will be at the bottom with depth of log n. Hence O(log n) * O(comp)
        """
        if current is not None:
            if current.left is None:
                return current
            else:
                return self.get_minimal(current.left)
    def get_subtree_size(self, current: TreeNode):
        """
        Get the subtree size
        Complexity:
        - Best case = Worst case: O(1), all constant
        """
        if current is not None:
            return current.subtree_size
        else:
            return 0

    def is_leaf(self, current: TreeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """

        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: TreeNode) -> TreeNode:
        """
        Finds the kth smallest value by key in the subtree rooted at current.
        Complexity:
        Best case : O(1) * O(comp), where O(comp) is complexity comparison, when the k value is length of the subtree.
        Root is the kth smallest.

        Worst case: O(log n) * O(comp) where n is the number of node in the tree, traverse to left/right subtree based on k
                                and continue traverse to left/right subtree until found the kth smallest. So is depends on
                                depth of the tree which is log n if is a balance tree.
        """
        if k >= 1 and k <= current.subtree_size:
            left_subtree_size = self.get_subtree_size(current.left)

            if k <= left_subtree_size:
                return self.kth_smallest(k, current.left)
            elif k == left_subtree_size + 1:
                return current
            else:
                return self.kth_smallest(k - left_subtree_size - 1, current.right)

