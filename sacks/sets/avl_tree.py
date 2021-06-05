from .binary_search_tree import BinarySearchTree
from ..primitives.avl_node import EMPTY

def rotate_right(root):
    r"""
    ```
      root    pivot
       /         \
    pivot -->   root
       \         /
        R       R
    ```
    """
    pivot = root.left
    root.left = pivot.right
    pivot.right = root

    root.balance -= 1 + pivot.balance  # Note pivot.balance >= 0
    pivot.balance -= 1

    return pivot

def rotate_left(root):
    r"""
    ```
    root        pivot
      \          /
     pivot --> root
      /          \
     L            L
    ```
    """
    pivot = root.right
    root.right = pivot.left
    pivot.left = root

    root.balance += 1 - pivot.balance  # Note pivot.balance <= 0
    pivot.balance += 1

    return pivot

def balance(root):
    if root.balance > 1:
        if root.left.balance < 0:
            root.left = rotate_left(root.left)
        return rotate_right(root)

    if root.right.balance > 0:
        root.right = rotate_right(root.right)
    return rotate_left(root)


# TODO: Implement join, split, union bulk operations. :class: Rope can inherit from AVLTree once implemented.

class AVLTree(BinarySearchTree):
    """
    A self-balancing binary search tree.

    Notes
    -----
    This version of an AVL tree allows multiple of the same item to be inserted.

    """
    __slots__ = ()

    def __init__(self, iterable=()):
        self._root = EMPTY
        self._len = 0

        self |= iterable

    @property
    def balance(self):
        return self._root.balance

    def rebalance(self, root, delta):
        """Rebalance the tree after a node addition or removal. (`delta` will be 1 for addition and -1 for removal.)
        """
        if not root:
            return

        if root is self._root:
            if root.balance in (-2, 2):
                self._root = balance(root)
                self._root.parent = EMPTY
            return

        if root.balance in (-2, 2):
            parent = root.parent
            if root.is_left_child:
                new_root = parent.left = balance(root)
            else:
                new_root = parent.right = balance(root)

            return self.rebalance(new_root, delta) if delta == -1 else None  # Keep recursing if node was deleted.

        root.parent.balance += delta if root.is_left_child else -delta

        if delta == 1 and root.parent.balance != 0 or delta == -1 and root.parent.balance not in (1, -1):
            self.rebalance(root.parent, delta)

    def add(self, item):
        self._root, new_node = self._root.add_key(item)
        self._len += 1
        self.rebalance(new_node, delta=1)

    def remove(self, item):
        self._root, unbalanced_node = self._root.remove_key(item)
        self._len -= 1
        self.rebalance(unbalanced_node, delta=-1)
