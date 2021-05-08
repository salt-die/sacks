from collections.abc import MutableSequence

from ..primitives import RopeInternal, RopeLeaf


class Rope(MutableSequence):
    """
    A binary-tree that allows efficient manipulation of variable-length types.

    Parameters
    ----------
    sequence (optional):
        Builds a Rope from the sequence if provided.  `type` is inferred from `sequence`'s type.

    leafsize:
        Max length of sequences stored in leaf nodes. (default: 8)

    type:
        Type of sequence stored in leaf nodes.  Inferred from `sequence` if a sequence is provided. (default: str)

    Notes
    -----
    The sequence type should have an `__add__` method.

    """
    __slots__ = '_root', 'leafsize', 'type',

    def __init__(self, sequence='', *, leafsize=8, type=None):
        self._root = RopeInternal()
        self.leafsize = leafsize
        self.type = type or __builtins__['type'](sequence)

        if sequence:
            raise NotImplementedError

    @property
    def sequence(self):
        return ''.join(self._root) if self.type is str else sum(self._root)

    def __len__(self):
        return self._root.weight

    def _collapse(self):
        """Remove all InternalNodes with EMPTY leaves.
        """
        raise self._root.collapse()

    def _balance(self):
        root = self._root

        if root.balance_factor > 1:
            if root.left.balance_factor < 0:
                root.left = self._rotate_left(root.left)  # left-right case
            self._root = self._rotate_right(root)
            self._balance()

        elif root.balance_factor < -1:
            if root.right.balance_factor > 0:
                root.right = self._rotate_right(root.right)  # right-left case
            self._root = self._rotate_left(root)
            self._balance()

    def _rotate_right(self, root):
        pivot = root.left
        root.left = pivot.right
        pivot.right = root
        return pivot

    def _rotate_left(self, root):
        pivot = root.right
        root.right = pivot.left
        pivot.left = root
        return pivot

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __add__(self, other):
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        new_rope = Rope(leafsize=max(self.leafsize, other.leafsize), type=self.type)
        new_rope._root.left = self._root.copy()
        new_rope._root.right = other._root.copy()
        return new_rope

    def __iadd__(self, other):
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        self._root = RopeInternal(self._root, other._root.copy())

    def join(self, other):
        self._root = RopeInternal(self._root, other._root)

    def insert(self, index, sequence):
        raise NotImplementedError

    def split(self, index):
        raise NotImplementedError

    def __repr__(self):
        return f'{type(self).__name__}({self.sequence!r}, leafsize={self.leafsize}, type={self.type.__name__})'

    def __str__(self):
        return str(self.sequence)

    def prettyprint(self):
        print(self._root)
