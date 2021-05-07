from collections.abc import MutableSequence

from ..primitives import RopeInternal, RopeLeaf


class Rope(MutableSequence):
    """
    A tree-like structure that allows efficient manipulation of variable-length types.

    Parameters
    ----------
    """
    __slots__ = '_root', 'leafsize', 'type',

    def __init__(self, sequence='', *, leafsize=8, type=None):
        self._root = RopeInternal()
        self.leafsize = leafsize
        self.type = type or type(sequence)

        if sequence:
            raise NotImplementedError

    def _balance(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __len__(self):
        return self.root.weight

    def insert(self, index, sequence):
        raise NotImplementedError

    def __add__(self, other):
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        new_rope = Rope(leafsize=max(self.leafsize, other.leafsize), type=self.type)
        new_rope.root.left = self.root.copy()
        new_root.root.right = other.root.copy()
        return new_rope

    def split(self, index):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
