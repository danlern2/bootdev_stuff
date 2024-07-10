from __future__ import annotations

# from typing import Any


class RBNode:
    """
    A node that goes on a Red/Black Tree structure.
    """

    def __init__(
        self: RBNode,
        val: int | None,
        left: None | RBNode = None,
        right: None | RBNode = None,
        red: bool = False,
    ):
        self.parent: RBNode | None = None
        self.val: int | None = val
        self.left: RBNode | None = left
        self.right: RBNode | None = right
        self.red = red

    def heights(self, initial: int | None = None):
        """
        This method returns the heights of the left and right side of the tree from a given node.
        """
        left: int = 0
        right: int = 0
        current = self
        while current and current.left is not None and current.left.val is not None:
            current = current.left
            left += 1
        current = self
        while current and current.right is not None and current.right.val is not None:
            current = current.right
            right += 1
        return left + 1, right + 1


# @dataclass
class RBTree:
    """
    - 𝗔 𝘀𝗲𝗹𝗳-𝗯𝗮𝗹𝗮𝗻𝗰𝗶𝗻𝗴 𝗯𝗶𝗻𝗮𝗿𝘆 𝘀𝗲𝗮𝗿𝗰𝗵 𝘁𝗿𝗲𝗲. 𝗘𝗮𝗰𝗵 𝗻𝗼𝗱𝗲 𝘀𝘁𝗼𝗿𝗲𝘀 𝗮𝗻 𝗲𝘅𝘁𝗿𝗮 𝗯𝗶𝘁, 𝘄𝗵𝗶𝗰𝗵 𝘄𝗲 𝘄𝗶𝗹𝗹 𝗰𝗮𝗹𝗹 𝘁𝗵𝗲 𝗰𝗼𝗹𝗼𝗿, 𝗿𝗲𝗱 𝗼𝗿 𝗯𝗹𝗮𝗰𝗸.
    - The color ensures that the tree remains approximately balanced during insertions and deletions.
    - When the tree is modified, the new tree is rearranged and repainted to restore the coloring properties that constrain how unbalanced the tree can become in the worst case.
    - - The re-balancing of a red-black tree does 𝘯𝘰𝘵 result in a perfectly balanced tree. However, its insertion and deletion operations, along with the tree rearrangement and recoloring, are always performed in O(log(n)) time.
    ### Properties
    - In addition to all the properties of a Binary Search Tree, a red-black tree must have the following:
    1. Each node is either red or black.
    2. The root is black. This rule is sometimes omitted. Since the root can always be changed from red to black, but not necessarily vice versa, this rule has little effect on analysis.
    3. All `nil` leaf nodes are black.
    4. If a node is red, then both its children are black.
    5. All paths from a single node go through the same number of black nodes to reach any of its descendant `nil` nodes.
    """

    # ? [assignments/binary_tree/redblackexample.png]

    def __init__(self, root: None | RBNode = None):
        self.nil = RBNode(None)
        # self.nil.red = False
        # self.nil.left = None
        # self.nil.right = None
        self.root = root or self.nil

    def insert(self, val: int):
        """
        ### An RBTree method to insert a new node.
        Instantiate a new RBNode with the given value.
        1. A new node will be a leafnode, so set its `left` and `right` children to nil.
        2. A node with black children must be red, so assign the new node to red.
        3. Initialize a `parent` variable as `None` (because we dont know it yet) and `current` variable as the root of the tree (*See step 5)
        4. While current is not a `nil` node, set parent to be current.
        - - Traverse the entire tree using comparisons,
          and set current to be its own child, until `current` is a `nil` node to find the node that has the closest value
          to our new node. (Duplicates are not allowed, so an equal comparison returns)
        5. If the parent is still `None`, the tree must be empty, so set the tree's root to the new node.
        - - Otherwise, assign the new node to be the parent's left or right child, depending on comparisons.
        """
        new_node = RBNode(val)
        new_node.left = self.nil  # type: ignore
        new_node.right = self.nil  # type: ignore
        new_node.red = True
        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.val < current.val:  # type: ignore
                current = current.left  # type: ignore
            elif new_node.val > current.val:  # type: ignore
                current = current.right  # type: ignore
            else:
                # * duplicate, just ignore
                return

        new_node.parent = parent  # type: ignore
        if parent is None:
            self.root = new_node
            new_node.red = False
            return
        else:
            if parent.val > new_node.val:  # type: ignore
                parent.left = new_node  # type: ignore
            elif parent.val < new_node.val:  # type: ignore
                parent.right = new_node  # type: ignore

        self.fix_insert(new_node)

    def fix_insert(self, new_node: RBNode):
        """
        As we insert nodes into the tree, we must be sure we keep the tree as shallow as possible. 
         This method will be automatically called after an insert to reshuffle the tree, recoloring as necessary and rotating as necessary.

        1. Loop until the new node isn't the root and its parent isn't black:
        2. Determine what type of child the parent is (left or right):
        3. If the parent is a right child:
        - Set uncle to parent's sibling.
        - If uncle is red:
        - - Recolor the parent, uncle, and grandparent.
        - - Move up the tree.
        - If uncle is black:
        - - If the new node is a left child, rotate right around parent.
        - - Adjust colors and rotate left around grandparent.
        4. If the parent is a left child:
        - Similar steps to above but mirrored (left/right swapped).
        5. Ensure the root is always black at the end.

        #### ? [assignments/binary_tree/redblackexample.png]
        ```
        # NOTE EXAMPLE TREE
                             [B] <- Grandparent
                            /   \\
         Parent (Red) ->  [R]    [U] <- Uncle (Red)
                         /
                       [N] <- New Node (Red)
        ```
        EXAMPLE STEPS:
        Step 1: Recolor parent and uncle to black, and grandparent to red.
        Step 2: Move up to the grandparent node and continue fixing if needed.
          If the uncle is black:
            Depending on the position of the new node (left or right child), rotate and recolor as part of the fix.
        """
        while (
            (new_node.parent != self.root and new_node.parent is not None)
            and new_node != self.root
            and new_node.parent.red is True
        ):
            if (
                new_node.parent.parent is not None
                and new_node.parent == new_node.parent.parent.right
            ):
                uncle: RBNode | None = new_node.parent.parent.left
                if uncle is not None and uncle.red:
                    uncle.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                elif uncle is not None and uncle.red is False:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.red = False  # type: ignore
                    new_node.parent.parent.red = True  # type: ignore
                    self.rotate_left(new_node.parent.parent)  # type: ignore

            elif (
                new_node.parent.parent is not None
                and new_node.parent == new_node.parent.parent.left
            ):
                uncle = new_node.parent.parent.right
                if uncle is not None and uncle.red:
                    uncle.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.red = False  # type: ignore
                    new_node.parent.parent.red = True  # type: ignore
                    self.rotate_right(new_node.parent.parent)  # type: ignore
        self.root.red = False

    def rotate_left(self: RBTree, x: RBNode | None):
        # ? Example [assignments/binary_tree/rotate.png]
        if x == self.nil or x.right == self.nil:  # type: ignore
            return
        y: RBNode = x.right  # type: ignore
        x.right = y.left  # type: ignore
        if y.left != self.nil:  # type: ignore
            y.left.parent = x  # type: ignore
        y.parent = x.parent  # type: ignore
        if x == self.root:
            self.root = y
        elif x == x.parent.left:  # type: ignore
            x.parent.left = y  # type: ignore
        elif x == x.parent.right:  # type: ignore
            x.parent.right = y  # type: ignore
        y.left = x  # type: ignore
        x.parent = y  # type: ignore

    def rotate_right(self: RBTree, x: RBNode | None):
        # ? Example [assignments/binary_tree/rotate.png]
        if x == self.nil or x.left == self.nil:  # type: ignore
            return
        y: RBNode = x.left  # type: ignore
        x.left = y.right  # type: ignore
        if y.right != self.nil:  # type: ignore
            y.right.parent = x  # type: ignore
        y.parent = x.parent  # type: ignore
        if x == self.root:
            self.root = y
        elif x == x.parent.left:  # type: ignore
            x.parent.left = y  # type: ignore
        elif x == x.parent.right:  # type: ignore
            x.parent.right = y  # type: ignore
        y.right = x  # type: ignore
        x.parent = y  # type: ignore

    def black_count(self, node: RBNode, blacks: set[int] = set(), counter: int = 0):
        """
        Starting from any node in the tree, this will traverse the tree and will count the number of times it passes through a black node, including the input node.
        - If the set contains more than 1 value, your tree is invalid.
        """
        if node.red is False:
            counter += 1
        if node.left:
            self.black_count(node.left, blacks, counter)
        if self.is_left(node):
            blacks.add(counter)
        if node.right:
            self.black_count(node.right, blacks, counter)
        if self.is_right(node):
            blacks.add(counter)
        if self.is_leaf(node):
            blacks.add(counter)
        return blacks

    def is_leaf(self, node: RBNode):
        if node.left == self.nil and node.right == self.root:
            return True
        return False

    def is_left(self, node: RBNode):
        if node == self.nil:
            return False
        if node.left != self.nil:
            return False
        current = self.root
        while current and current.left != self.nil:
            current = current.left
        if current == node:
            return True
        return False

    def is_right(self, node: RBNode):
        if node == self.nil:
            return False
        if node.right != self.nil:
            return False
        current = self.root
        while current and current.right != self.nil:
            current = current.right
        if current == node:
            return True
        return False


# def n(t: RBTree, val: int, left=None, right=None, red: bool = False) -> RBNode:  # type: ignore
#     return RBNode(val, left=left or t.nil, right=right or t.nil, red=red)  # type: ignore


# def test_6_rbtree():
# import random
#     test_tree = RBTree()
#     range_list = list(range(1, 30))
#     random.seed(10)
#     random.shuffle(range_list)
#     for i in range_list:
#         test_tree.insert(i)

#     t = RBTree()
#     t.root = RBNode(3)
#     t.root.left = n(t, 2, left=n(t, 1, red=True), red=False)
#     t.root.right = n(t, 4, right=n(t, 5, red=True), red=False)

#     print(test_tree.black_count(test_tree.root))


# test_6_rbtree()
