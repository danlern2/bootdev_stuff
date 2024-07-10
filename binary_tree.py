from __future__ import annotations
from typing import List, Any
# from dataclasses import dataclass, field


class BinarySearchTree:
    """
    ## BINARY SEARCH TREE
    Trees aren't particularly useful data structures unless they're ordered in some way. One of the most
    common types of ordered tree is a Binary Search Tree or BST. In addition to the properties we've already talked about, a
    BST has some additional constraints:

    1. Instead of a list of children, each node has at most 2 children, a right and a left child
    2. The left child's value must be less than its parent's value
    3. The right child's value must be greater than its parents
    4. No two nodes in the BST can have the same value

    - An ordered binary tree, that is deeper than it is wide, will be O(n) for operations performed on it.
    - - The BSTNode class is a normal BST, and allows for this to occur.
    - - See RBTree below for an alternative type of BST.
    """

    pass


class BSTNode:
    """
    The building blocks of a BST are Nodes. In our implementation, we will only use a single class, the `BSTNode` class.
    Any `BSTNode` is technically also a full Binary Search Tree, with itself as the root node. Each method that traverses
    the tree will do so recursively.
    """

    def __init__(self, val: int | None = None):  # type: ignore
        self.left: BSTNode | None = None
        self.right: BSTNode | None = None
        self.val: int | None = val

    def insert(self, val: int):
        if self.val is None:
            self.val = val
            return
        if self.val == val:
            return
        if val < self.val:
            if self.left is None:
                self.left = BSTNode(val)
                return
            self.left.insert(val)
            return
        if val > self.val:
            if self.right is None:
                self.right = BSTNode(val)
                return
            self.right.insert(val)
            return

    def get_min(self: BSTNode) -> int | None:
        current: BSTNode = self
        while current.left is not None:
            current: BSTNode = current.left
        return current.val

    def get_max(self: BSTNode) -> int:
        current: BSTNode = self
        while current.right is not None:
            current: BSTNode = current.right
        return current.val  # type: ignore

    def height(self) -> int:
        """
        This method returns the maximum height of the tree from a given node, recursively.
        """
        if self.val is None:
            return 0
        left: int = 0
        right: int = 0
        if self.left:
            left = self.left.height()
        if self.right:
            right = self.right.height()
        return max(left, right) + 1

    def delete(self, val: int) -> BSTNode | None:
        """
        #### Given a value on the tree, this method will search the binary tree in O(log(n)) for the node that has the input value, and then it will delete it by changing what the parent points to.
        1. Check if the current node's value (`self.val`) is `None`.
        2. If the input is less than the current node's value, it must be down the left side of the tree:
        - - If the left child is not empty, then what we are looking for must be further down, so recursively search that subtree, and take the result and change the current pointer to the returned node.
        - - Return the current node
        3. Do the same operation, if it is greater, on the right.
        4. If the value to delete is equal to the current node's value, we have found the node we want to delete:
        - - If there is no right child, return the left child. This effectively deletes the current node by bypassing it.
        - - If there is no left child, return the right child. This effectively deletes the current node by bypassing it.
        - - If there are both left and right children, find the minimum larger node (`min_larger_node`) by traversing down the left side of the right subtree. This is the node with the smallest value that is still larger than `self.val`.
        - - - Replace `self.val` with `min_larger_node.val`.
        - - - Delete `min_larger_node.val` from the right subtree and set the right child to the return value of the recursive call.
        5. Return the current node.
        """
        if self.val is None:
            return None
        elif val < self.val:
            if self.left is not None:
                self.left = self.left.delete(val)
            return self
        elif val > self.val:
            if self.right is not None:
                self.right = self.right.delete(val)
            return self
        elif val == self.val:
            if self.right is None:
                return self.left
            if self.left is None:
                return self.right
        min_larger_node: BSTNode = self.right  # type: ignore
        while min_larger_node.left:  # * Evaluates to true if its not None
            min_larger_node = min_larger_node.left
            self.val = min_larger_node.val
            self.right = self.right.delete(min_larger_node.val)  # type: ignore
        return self

    def preorder(self, visited: List[Any] = []) -> List[Any]:
        """
        Starting from any node in the tree, this will traverse the tree and will return a list of values in the order in
        which a node was visited, from the top down.
        """
        visited.append(self.val)
        if self.left:
            self.left.preorder(visited)
        if self.right:
            self.right.preorder(visited)
        return visited

    def postorder(self, visited: List[Any] = []) -> List[Any]:
        """
        Starting from any node in the tree, this will traverse the tree and will return a list of values in the order in
        which a node was visited, from the bottom up.
        """
        if self.left:
            self.left.postorder(visited)
        if self.right:
            self.right.postorder(visited)
        visited.append(self.val)
        return visited

    def inorder(self, visited: List[Any] = []) -> List[Any]:
        """
        Starting from any node in the tree, this will traverse the tree and will append the values on the left side of
        every subtree, and return a list ordered from highest to lowest by value rather than position.
        """
        if self.left:
            self.left.inorder(visited)
        visited.append(self.val)
        if self.right:
            self.right.inorder(visited)
        return visited

    def exists(self: BSTNode, val: int) -> bool:
        """
        Given a value, this method will search the tree in O(log(n)) for the node that has the input value and returns whether it exists.
        """
        if self.val == val:
            return True
        if val < self.val:  # type: ignore
            if self.left:
                return self.left.exists(val)
        if val > self.val:  # type: ignore
            if self.right:
                return self.right.exists(val)
        return False

    def search_range(self, lower_bound: int, upper_bound: int) -> List[int]:
        """
        Returns a preordered list.\n
        Given an upper bound value and a lower bound value, will print a list of all the values in the range.
        """
        result: list[int] = []
        if self.val is None:
            return result
        if lower_bound <= self.val <= upper_bound:
            result.append(self.val)
        if self.left and self.val > lower_bound:
            result.extend(self.left.search_range(lower_bound, upper_bound))
        if self.right and self.val < upper_bound:
            result.extend(self.right.search_range(lower_bound, upper_bound))
        return result
