from collections.abc import MutableSequence
from functools import wraps

from ..primitives import RopeInternal, RopeLeaf


class Rope(MutableSequence):
    """
    A binary-tree that allows efficient manipulation of variable-length types.

    Parameters
    ----------
    sequence (optional):
        Builds a Rope from the sequence if provided. `type` is inferred from `sequence`'s type.

    leafsize:
        Max length of sequences stored in leaf nodes. (default: 8)

    type:
        Type of sequence stored in leaf nodes. Inferred from `sequence` if a sequence is provided. (default: str)

    Notes
    -----
    The sequence type should have an `__add__` method.

    """
    __slots__ = '_root', 'leafsize', 'type', '_len',

    def __init__(self, sequence='', *, leafsize=8, type=None):
        self._root = RopeInternal()
        self.leafsize = leafsize
        self.type = type or __builtins__['type'](sequence)
        self._len = len(sequence)

        if sequence:
            self._from_sequence(sequence, self._root)
            self._collapse()
            self.balance()

    def _from_sequence(self, sequence, root):
        size = len(sequence)
        if size <= self.leafsize:
            root.left = RopeLeaf(sequence)
        elif size <= self.leafsize * 2:
            root.left = RopeLeaf(sequence[:size//2])
            root.right = RopeLeaf(sequence[size//2:])
        else:
            root.left = RopeInternal()
            root.right = RopeInternal()
            self._from_sequence(sequence[:size//2], root.left)
            self._from_sequence(sequence[size//2:], root.right)

    @property
    def sequence(self):
        return ''.join(self._root) if self.type is str else sum(self._root)

    def copy(self):
        copy = Rope(leafsize=self.leafsize, type=self.type)
        copy._root = self._root.copy()
        return copy

    def __len__(self):
        return self._len

    def _collapse(self):
        """Replace all RopeInternal nodes with EMPTY leaves with their non-EMPTY child.
        """
        self._root.collapse()

    def balance(self):
        self._root = self._balance(self._root)

    def _balance(self, root):
        if not isinstance(root, RopeInternal):
            return root

        root.left = self._balance(root.left)
        root.right = self._balance(root.right)

        factor = root.balance_factor
        if factor > 1:
            if root.left.balance_factor < 0:
                root.left = self._rotate_left(root.left)  # left-right case
            root = self._rotate_right(root)

        elif factor < -1:
            if root.right.balance_factor > 0:
                root.right = self._rotate_right(root.right)  # right-left case
            root = self._rotate_left(root)

        return root

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

    def __iter__(self):
        for seq in self._root:
            yield from seq

    def _normalize_index(self, index):
        """Common functionality for parsing slices for __getitem__, __setitem__, and __delitem__.
        """
        if isinstance(index, int):
            if index > len(self):
                raise IndexError('index out of range')
            start, stop, step = index, index + 1, 1
        else:
            start, stop, step = index.indices(len(self))

        if step != 1:
            raise ValueError('invalid step')

        if start >= stop:
            raise ValueError('0-length slice not supported')

        return start, stop - start

    def __getitem__(self, key):
        first_split, second_split = self._normalize_index(key)

        #FIXME: This is inefficient
        _, other = self.split(first_split)
        _, end = other.split(second_split)

        sequence = other.sequence
        self.join(other)
        self.join(end)
        return sequence

    def __setitem__(self, key, sequence):
        first_split, second_split = self._normalize_index(key)

        self._len -= second_split + len(sequence)

        _, other = self.split(first_split)
        _, end = other.split(second_split)
        self.join(Rope(sequence, leafsize=self.leafsize))
        self.join(end)

    def __delitem__(self, key):
        first_split, second_split = self._normalize_index(key)

        self._len -= second_split

        _, other = self.split(first_split)
        _, end = other.split(second_split)
        self.join(end)

    def __add__(self, other):
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        new_rope = Rope(leafsize=max(self.leafsize, other.leafsize), type=self.type)
        new_rope._root = self._root.copy()
        new_rope += other
        new_rope._len = len(self) + len(other)
        return new_rope

    def __iadd__(self, other):
        self.join(other.copy())
        self._len += len(other)
        return self

    def append(self, sequence):
        self += Rope(sequence, leafsize=self.leafsize)
        self._len += len(sequence)

    def join(self, other):
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        self._len += len(other)

        # FIXME: This is inefficient
        self._root = RopeInternal(self._root, other._root)
        self.balance()
        # if self._root.height == other._root.height:
        #     self._root = RopeInternal(self._root, other._root)
        # elif self._root.height > other._root.height:
        #     self._join_right(self, other)
        # else:
        #     self._join_left(self, other)

    def _join_right(self, other):
        raise NotImplementedError

    def _join_left(self, other):
        raise NotImplementedError

    def insert(self, index, sequence):
        self._len += len(sequence)
        _, end = self.split(index)
        self.join(Rope(sequence, leafsize=self.leafsize))
        self.join(end)

    def split(self, index):
        right = Rope(leafsize=self.leafsize)
        right._root = self._root.split(index)
        right.balance()
        self.balance()

        right._len = self._len - index
        self._len = index

        return self, right

    def __repr__(self):
        return f'{type(self).__name__}({self.sequence!r}, leafsize={self.leafsize}, type={self.type.__name__})'

    def __str__(self):
        return str(self.sequence)

    def prettyprint(self):
        print(self._root)
