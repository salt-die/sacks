from bisect import bisect_left, bisect_right, insort
from collections.abc import MutableSet, Sequence
from math import ceil, log2, inf

from . import Column

def pair_sum(iterator):
    """Generate sum of consecutive pairs from iterator.
    """
    while (i := next(iterator, inf) + next(iterator, inf)) != inf:
        yield i


class SortedList(MutableSet, Sequence):
    """An ordered sequence using Python's built-in types. (A slim version of https://github.com/grantjenks/python-sortedcontainers/.)
    """
    __slots__ = '_lists', '_maxes', '_weights', '_len', '_load',

    DEFAULT_LOAD = 10

    def __init__(self, iterable=(), *, load=DEFAULT_LOAD):
        self._lists = []
        self._maxes = Column(-1, self._lists)
        self._weights = []

        self._len = 0
        self._load = load

        self |= iterable

    def __contains__(self, item):
        if not self:
            return False

        lists = self._lists

        i = bisect_left(self._maxes, item)

        if i == len(lists):
            return False

        j = bisect_left(lists[i], item)

        return lists[i][j] == value

    def __iter__(self):
        for sublist in self._lists:
            yield from sublist

    def __reversed__(self):
        for sublist in reversed(self._lists):
            yield from reversed(sublist)

    def __len__(self):
        return self._len

    def add(self, item):
        lists = self._lists

        if lists:
            i = bisect_right(self._maxes, item)

            if i == len(lists):
                i -= 1
                lists[i].append(item)
            else:
                insort(lists[i], item)

            self._expand(i)
        else:
            lists.append( [item] )

        self._len += 1

    def remove(self, item):
        if not self:
            raise KeyError(item)

        lists = self._lists

        i = bisect_left(self._maxes, item)

        if i == len(lists):
            raise KeyError(item)

        j = bisect_left(lists[i], item)

        if lists[i][j] != item:
            raise KeyError(item)

        self._delete(i, j)

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def pop(self, index=-1):
        """Remove and return item at index.
        """
        lists = self._lists

        if index == -1:
            i, j = len(lists) - 1, -1
        elif index == 0:
            i, j = 0, 0
        else:
            i, j = self._coord(index)

        try:
            return lists[i][j]
        finally:
            self._delete(i, j)

    def clear(self):
        self._lists.clear()
        self._weights.clear()

    def index(self, item):
        """Return first index of item `i`.
        """
        if not self:
            raise KeyError(item)

        lists = self._lists

        i = bisect_left(self._maxes, item)

        if i == len(lists):
            raise ValueError(f'{item} is not in {type(self).__name__}')

        j = bisect_left(lists[i], item)

        if lists[i][j] != item:
            raise ValueError(f'{item} is not in {type(self).__name__}')

        return self._index(i, j)

    def __getitem__(self, index):
        i, j = self._coord(index)

        return self._lists[i][j]

    def __delitem__(self, index):
        self._delete(*self._coord(index))

    def _expand(self, i):
        """Split sublist `i` if its size is greater than double _load.
        """
        load = self._load
        lists = self._lists

        if len(lists[i]) > load << 1:
            sub = lists[i]
            half = sub[load:]

            del sub[load:]

            lists.insert(i + 1, half)
            self._weights.clear()

        else:
            self._weight_update(i, 1)

    def _shrink(self, i):
        """Combine sublist 'i' if its size is less than half _load.
        """
        lists = self._lists

        if len(lists[i]) < self._load >> 1 and len(lists) > 1:
            i = max(i, 1)

            lists[i - 1].extend(lists[i])

            del lists[i]
            self._weights.clear()

            self._expand(i - 1)

        else:
            self._weight_update(i, -1)

    def _delete(i, j):
        """Delete item `j` in sublist `i`.
        """
        del self._lists[i][j]
        self._shrink(i)
        self._len -= 1

    def _weight_update(self, i, delta):
        """Increment weights of leaf `i` and all its ancestors in _weights by delta.
        """
        weights = self._weights
        if not weights:
            return

        i -= len(weights)
        while i != -1:
            weights[i] += delta
            i >>= 1

    def _coord(self, index):
        """Return the pair (i, j) such that `_lists[i][j]` has given index.
        """
        if not isinstance(index, int):
            raise TypeError(f'index must be int, not {type(index).__name__}')

        _, j, _ = slice(index).indices(len(self))
        if j >= len(self):
            raise IndexError('index out of range')

        weights = self._weights

        if not weights:
            self._build_weights()

        i = -1
        for _ in range(weights[-1]):
            i <<= 1
            if j >= weights[i]:
                j -= weights[i]
                i += 1

        i += len(weights)

        return i, j

    def _index(self, i, j):
        """Inverse of `_coord`. Return index of _lists[i][j].
        """
        return sum(len(self._lists[k]) for k in range(i)) + j

    def _build_weights(self):
        """
        Each length of a list in _lists is a leaf in a binary-tree (padded with `0`s until the number of
        leaves is equal to the nearest power of 2). Parent nodes are added between consecutive leaves with
        weight equal to the sum of their children.  Similarly, parents of consecutive parents are added,
        until a single root is reached.

        The last item of `_weights` is the level of the tree.

        Nodes on level i start at index -1 << i + 1. (Level 0 at index -2 is the root with weight equal to
        length of the sorted list.)

        """
        weights = self._weights
        lists = self._lists

        n_lists = len(lists)
        height = ceil(log2(n_lists))

        base = list(map(len, lists))
        base.extend(0 for _ in range((1 << height) - n_lists))

        while base:
            weights.extend(base)
            base =tuple(pair_sum( iter(base) ))

        weights.append(height + 1)

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}])'
