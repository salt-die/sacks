# TODO: Keep track of how "messy" a tree is so we can coalesce many short leaves and rebalance.
from collections.abc import MutableSequence

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
    The sequence type should be sliceable and have an `__add__` method.

    """
    __slots__ = '_root', 'leafsize', 'type', '_len',

    def __init__(self, sequence='', *, leafsize=8, type=None):
        self._root = RopeInternal()
        self.leafsize = leafsize
        self.type = type or __builtins__['type'](sequence)
        self._len = len(sequence)

        if sequence:
            self._from_sequence(sequence, self._root)
            self.collapse()

    def _from_sequence(self, sequence, root):
        size = len(sequence)

        if size <= self.leafsize * 2:
            root.left = RopeLeaf(sequence[:size//2])
            root.right = RopeLeaf(sequence[size//2:])
        else:
            root.left = RopeInternal()
            root.right = RopeInternal()
            self._from_sequence(sequence[:size//2], root.left)
            self._from_sequence(sequence[size//2:], root.right)

    def __len__(self):
        return self._len

    def __iter__(self):
        for seq in self._root:
            yield from seq

    @property
    def sequence(self):
        """A monolithic sum of all the leaves of this rope.
        """
        return ''.join(self._root) if self.type is str else sum(self._root, self.type())

    @property
    def balance_factor(self):
        """The difference in heights of the left and right sides of this rope.
        """
        return self._root.balance_factor

    def copy(self):
        """Return a copy of this rope.
        """
        copy = Rope(leafsize=self.leafsize, type=self.type)
        copy._root = self._root.copy()
        copy._len = self._len
        return copy

    def collapse(self):
        """Remove all non-internal 0 weight nodes.
        """
        self._root.collapse()

    def balance(self):
        """Balance the tree.
        """
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

    def _normalize_index(self, index):
        """Common functionality for parsing slices for __getitem__, __setitem__, and __delitem__.
        """
        if isinstance(index, int):
            if index < -len(self) or index >= len(self):
                raise IndexError('index out of range')

            if index < 0:
                index += len(self)

            start, stop, step = index, index + 1, 1
        else:
            start, stop, step = index.indices(len(self))

        if step != 1:
            raise ValueError('invalid step')

        if start >= stop:
            raise ValueError('0-length slice not supported')

        return start, stop - start

    def __getitem__(self, key):
        start, length = self._normalize_index(key)

        if self.type is str:
            return "".join(self._root.slice(start, length))

        return sum(self._root.slice(start, length), self.type())

    def __setitem__(self, key, sequence):
        first_split, second_split = self._normalize_index(key)

        _, other = self.split(first_split)
        _, end = other.split(second_split)

        self.join(Rope(sequence, leafsize=self.leafsize))
        self.join(end)
        self.collapse()

    def __delitem__(self, key):
        first_split, second_split = self._normalize_index(key)

        _, other = self.split(first_split)
        _, end = other.split(second_split)

        self.join(end)
        self.collapse()

    def __add__(self, other):
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        new_rope = Rope(leafsize=max(self.leafsize, other.leafsize), type=self.type)
        new_rope._root = self._root.copy()
        new_rope._len = len(self)
        new_rope += other
        return new_rope

    def __iadd__(self, other):
        self.join(other.copy())
        return self

    def append(self, sequence):
        """Append the sequence to the end of the rope.
        """
        self.join(Rope(sequence, leafsize=self.leafsize))

    def join(self, other):
        """
        Join `other` to this rope.

        Warning
        -------
        This doesn't copy.  `other` will be a view inside `self` or vice-versa.  Modifications to one will affect the other.

        """
        if self.type != other.type:
            raise TypeError(f'Incompatible types: {self.type}, {other.type}')

        balance = self._root.height - other._root.height

        if balance < -1:
            self._join_right(other, balance)
        elif balance > 1:
            self._join_left(other, balance)
        else:
            self._root = RopeInternal(self._root, other._root)

        self._len += len(other)

    def _join_right(self, other, balance):
        left_most = other._root
        while balance < 0:
            if isinstance(left_most, RopeInternal):
                left_most = left_most.left
                balance += 1
            else: # Either `other` isn't balanced or the left-most path is too short.  Either way, we're done.
                break

        left_most.strand.attach(RopeInternal(self._root, left_most))
        self._root = other._root

    def _join_left(self, other, balance):
        right_most = self._root
        while balance > 0:
            if isinstance(right_most, RopeInternal):
                right_most = right_most.right
                balance -= 1
            else: # Either `self` isn't balanced or the right-most path is too short.  Either way, we're done.
                break

        right_most.strand.attach(RopeInternal(right_most, other._root))

    def insert(self, index, sequence):
        """Insert sequence before `index`.
        """
        index, _ = self._normalize_index(index)

        _, end = self.split(index)
        self.join(Rope(sequence, leafsize=self.leafsize))
        self.join(end)

    def split(self, index):
        """Split the rope at `index`.  Return both ends of split.
        """
        index, _ = self._normalize_index(index)

        right = Rope(leafsize=self.leafsize, type=self.type)
        right._root = self._root.split(index)
        right._len = self._len - index
        right.collapse()

        self._len = index
        self.collapse()

        return self, right

    def __repr__(self):
        return f'{type(self).__name__}({self.sequence!r}, leafsize={self.leafsize}, type={self.type.__name__})'

    def __str__(self):
        return str(self.sequence)

    def prettyprint(self):
        print(self._root)
