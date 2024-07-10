from __future__ import annotations
from rb_tree import RBTree, RBNode
import random


def print_tree(tree: RBTree):
    lines: list[str] = []
    format_tree_string(tree.root, lines)
    return "\n".join(lines)


def format_tree_string(node: RBNode, lines: list[str], level: int = 0):
    if node.val is not None:
        format_tree_string(node.right, lines, level + 1)  # type: ignore
        lines.append(
            " " * 4 * level
            + "> "
            + str(node.val)
            + " "
            + ("[red]" if node.red else "[black]")
        )
        format_tree_string(node.left, lines, level + 1)  # type: ignore


def print_tree_height(tree: RBTree):
    print(f"Left side is {tree.root.heights()[0]} deep.")
    print(f"Right side is {tree.root.heights()[1]} deep.\n")


def n(t: RBTree, val: int, left=None, right=None, red: bool = False) -> RBNode:  # type: ignore
    return RBNode(val, left=left or t.nil, right=right or t.nil, red=red)  # type: ignore


# ===================Helper functions above===============


def test_4_rbtree():
    test_tree = RBTree()
    range_list = list(range(1, 4))
    random.seed(10)
    random.shuffle(range_list)
    for i in range_list:
        test_tree.insert(i)

    t = RBTree()
    t.root = n(t, 2, left=n(t, 1, red=True), right=n(t, 3, red=True))

    print(f"test_tree:\n\n {print_tree(test_tree)}\n")
    print_tree_height(test_tree)
    print(f"test_3deep_uneven_rbtree: \n\n{print_tree(t)}\n")
    print_tree_height(t)

    assert print_tree(test_tree) == print_tree(t)
    # assert False


def test_6_rbtree():
    test_tree = RBTree()
    range_list = list(range(1, 6))
    random.seed(10)
    random.shuffle(range_list)
    for i in range_list:
        test_tree.insert(i)

    t = RBTree()
    t.root = n(
        t,
        3,
        left=n(t, 2, left=n(t, 1, red=True), red=False),
        right=n(t, 4, right=n(t, 5, red=True), red=False),
    )

    print(f"test_tree:\n\n {print_tree(test_tree)}\n")
    print_tree_height(test_tree)
    print(f"test_3deep_uneven_rbtree: \n\n{print_tree(t)}\n")
    print_tree_height(t)

    assert print_tree(test_tree) == print_tree(t)
    # assert False


def test_15_rbtree():
    test_tree = RBTree()
    range_list = list(range(1, 30))
    random.seed(10)
    random.shuffle(range_list)
    for i in range_list:
        test_tree.insert(i)

    t = RBTree()
    t.root = n(
        t,
        6,
        left=n(
            t,
            3,
            left=n(t, 2, left=n(t, 1, red=True), right=None, red=False),
            right=n(t, 5, left=n(t, 4, red=True), right=None, red=False),
            red=False,
        ),
        right=n(
            t,
            11,
            left=n(
                t,
                8,
                left=n(t, 7, red=False),
                right=n(t, 9, right=n(t, 10, red=True), red=False),
                red=True,
            ),
            right=n(
                t, 13, left=n(t, 12, red=True), right=n(t, 14, red=True), red=False
            ),
            red=False,
        ),
    )

    print(f"test_tree:\n\n {print_tree(test_tree)}\n")
    print_tree_height(test_tree)
    print(f"{test_tree.black_count(test_tree.root)}\n")
    print(f"test_3deep_uneven_rbtree: \n\n{print_tree(t)}\n")
    print_tree_height(t)
    print(f"{t.black_count(t.root)}\n")

    assert print_tree(test_tree) == print_tree(t)
    assert False
