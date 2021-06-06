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
    __slots__ = '_lists', '_maxes', '_weights', '_len', '_load',

    DEFAULT_LOAD = 10

    def __init__(self, iterable=(), *, load=None):
        self._lists = []
        self._maxes = Column(-1, self._lists)
        self._weights = []

        self._len = 0
        self._load = load or self.DEFAULT_LOAD

        self |= iterable

    def __len__(self):
        return self._len

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

    def _expand(self, i):
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

        del lists[i][j]
        self._shrink(i)
        self._len -= 1

    def _shrink(self, i):
        load  = self._load
        lists = self._lists

        if len(lists[i]) < load >> 1 and len(lists) > 1:
            i = min(i, 1)

            lists[i - 1].extend(lists[i])

            del lists[i]
            self._weights.clear()

            self._expand(i - 1)
        else:
            self._weight_update(i, -1)

    def _weight_update(self, i, delta):
        weights = self._weights
        if not weights:
            return

        i -= len(weights)
        while i != -1:
            weights[i] += delta
            i >>= 1

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def clear(self):
        self._lists.clear()
        self._weights.clear()

    def __getitem__(self, index):
        i, j = self._coord(index)

        return self._lists[i][j]

    def __delitem__(self, index):
        i, j = self._coord(index)

        del self._lists[i][j]
        self._shrink(i)
        self._len -= 1

    def _coord(self, index):
        if not isinstance(index, int):
            raise KeyError(index)

        _, j, _ = slice(index).indices(len(self))
        if j >= len(self):
            raise KeyError(index)

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

    def _build_weights(self):
        weights = self._weights
        weights.clear()

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
