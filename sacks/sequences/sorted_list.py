from bisect import bisect_left, bisect_right, insort
from collections.abc import MutableSet, Sequence
from math import ceil, log2

def pair_sum(iterable):
    """Generate sum of consecutive pairs from iterable.
    """
    for item in (it := iter(iterable))
        yield item + next(it)


class SortedList(MutableSet, Sequence):
    __slots__ = '_lists', '_weights', '_len', '_load',

    DEFAULT_LOAD = 10

    def __init__(self, iterable=(), *, load=None):
        self._lists = []
        self._weights = []

        self._len = 0
        self._load = load or self.DEFAULT_LOAD

        self |= iterable

    def __len__(self):
        return self._len

    def __contains__(self, item):
        lists = self._lists

        if not (maxes := _MaxView(lists)):
            return False

        i = bisect_left(maxes, item)

        if i == len(maxes):
            return False

        j = bisect_left(lists[j], item)

        return lists[i][j] == value

    def __iter__(self):
        for sublist in self._lists:
            yield from sublist

    def __reversed__(self):
        for sublist in reversed(self._lists):
            yield from reversed(sublist)

    def add(self, item):
        lists = self._lists

        if maxes := _MaxView(lists):
            i = bisect_right(maxes, item)

            if i == len(maxes):
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
        weights = self._weights

        if len(lists[i]) > load << 1:
            sub = lists[i]
            half = sub[load:]

            del sub[load:]

            lists.insert(i + 1, half)

        if len(lists) <= len(weights) >> 1:
            i -= len(weights)
            while i < -2:
                weights[i] += 1
                i >>= 1
        else:
            weights.clear()

    def remove(self, item):
        ...

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def __getitem__(self, i):
        if not isinstance(i, int):
            raise KeyError(i)

        _, i, _ = slice(i).indices(len(self))
        if i >= len(self):
            raise KeyError(i)

        if not (weights := self._weights):
            self._build_weights()

        weights = self._weights
        node = -1

        for _ in range(weights[-1]):
            node <<= 1
            if i >= weights[node]:
                i -= weights[node]
                node += 1

        return self._lists[node][i]

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
            base = [a + b for a, b in chunk_by_2(base)]

        weights.append(height + 1)

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}]'
