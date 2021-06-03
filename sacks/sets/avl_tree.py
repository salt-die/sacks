from .binary_search_tree import BinarySearchTree
from ..primitives.avl_node import EMPTY

def rotate_right(root):
    r"""
      root    pivot
       /         \
    pivot -->   root
       \         /
        R       R
    """
    pivot = root.left
    root.left = pivot.right
    pivot.right = root

    if pivot.balance == 0:
        root.balance = -1
        pivot.balance = 1
    else:
        root.balance = pivot.balance = 0

    return pivot

def rotate_left(root):
    r"""
    root        pivot
      \          /
     pivot --> root
      /          \
     L            L
    """
    pivot = root.right
    root.right = pivot.left
    pivot.left = root

    if pivot.balance == 0:
        root.balance = 1
        pivot.balance = -1
    else:
        root.balance = pivot.balance = 0

    return pivot

def balance(root):
    if root.balance > 1:
        if root.left.balance < 0:
            root.left = rotate_left(root.left)
        return rotate_right(root)

    if root.right.balance > 0:
        root.right = rotate_right(root.right)
    return rotate_left(root)


class AVLTree(BinarySearchTree):
    """A self-balancing binary search tree.
    """
    def __init__(self, iterable=()):
        self.root = EMPTY
        self._len = 0

        self |= iterable

    @property
    def balance(self):
        return self.root.balance

    def update_balances(self, root, delta):
        if root is None:
            return

        if abs(root.balance) > 1:
            if root is self.root:
                self.root = balance(root)
                self.root.parent = None
            else:
                setattr(root.parent, 'left' if root.is_left_child else 'right', balance(root))

            return

        if root is self.root:
            return

        if root.is_left_child:
            root.parent.balance += 1 * delta
        else:
            root.parent.balance -= 1 * delta

        if root.parent.balance != 0:
            self.update_balances(root.parent, delta)

    def add(self, item):
        self.root, unbalanced_node = self.root.add_key(item)
        self._len += 1

        self.update_balances(unbalanced_node, 1)

    def remove(self, item):
        self.root, unbalanced_node = self.root.remove_key(item)
        self._len -= 1

        self.update_balances(unbalanced_node, -1)
