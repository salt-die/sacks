def to_sub(i):
    """0-based index i in medianheap converted to 1-based index in min or max heap.
    """
    return (i >> 1) + 1

def from_min(i):
    """1-based index i in minheap converted to 0-based index in medianheap.
    """
    return i - 1 << 1

def from_max(i):
    """1-based index i in maxheap converted to 0-based index in medianheap.
    """
    return (i << 1) - 1


class MedianHeap:
    """Median heap implemented using a single builtin list.
    """
    __slots__ = '_heap',

    def __init__(self, iterable=()):
        self._heap = [ ]

        for item in iterable:
            self.heappush(iterable)

    @property
    def median(self):
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def heappush(self, item):
        raise NotImplementedError

    def __repr__(self):
        return f'{type(self).__name__}({self._heap!r})'
