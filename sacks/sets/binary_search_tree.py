from collections.abc import MutableSet, Reversible

from ..primitives.bst_node import EMPTY


class BinarySearchTree(MutableSet, Reversible):
    """
    A binary tree with O(log n) containment, addition and deletion of items.

    Notes
    -----
    This version of a BST allows multiple of the same item to be inserted.

    """
    __slots__ = '_root', '_len',

    def __init__(self, iterable=()):
        self._root = EMPTY
        self._len = 0

        self |= iterable

    @property
    def root(self):
        return self._root

    @property
    def min(self):
        if not self:
            raise ValueError('tree is empty')

        current = self._root

        while current.left:
            current = current.left

        return current.key

    @property
    def max(self):
        if not self:
            raise ValueError('tree is empty')

        current = self._root

        while current.right:
            current = current.right

        return current.key

    def __len__(self):
        return self._len

    def __contains__(self, item):
        return item in self._root

    def __iter__(self):
        yield from self._root

    def __reversed__(self):
        yield from reversed(self._root)

    def add(self, item):
        self._root = self._root.add_key(item)
        self._len += 1

    def remove(self, item):
        self._root = self._root.remove_key(item)
        self._len -= 1

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}])'

    def __str__(self):
        return str(self._root)
