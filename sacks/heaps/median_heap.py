from heapq import (
    heappop as heappop_min,
    heappush as heappush_min,
    _heappop_max as heappop_max,
    _siftdown_max,
)

def heappush_max(heap, item):
    """Push item onto heap, maintaining the heap invariant.
    """
    heap.append(item)
    _siftdown_max(heap, 0, len(heap) - 1)


class MedianHeap:
    """Median heap implemented using two builtin lists.
    """
    __slots__ = '_maxheap', '_minheap',

    def __init__(self, iterable=()):
        self._maxheap = [ ]
        self._minheap = [ ]

        for item in iterable:
            self.heappush(iterable)

    def __len__(self):
        return len(self._maxheap) + len(self._minheap)

    @property
    def median(self):
        maxheap = self._maxheap
        minheap = self._minheap

        if len(maxheap) < len(minheap):
            return minheap[0]

        return maxheap[0]

    def heappop(self):
        maxheap = self._maxheap
        minheap = self._minheap

        if len(maxheap) < len(minheap):
            return heappop_min(minheap)

        return heappop_max(maxheap)

    def heappush(self, item):
        maxheap = self._maxheap
        minheap = self._minheap

        if not self:
            return minheap.append(item)

        if item > self.median:
            heappush_min(minheap, item)
        else:
            heappush_max(maxheap, item)

        if len(maxheap) - len(minheap) > 1:
            heappush_min(minheap, heappop_max(maxheap))
        elif len(minheap) - len(maxheap) > 1:
            heappush_max(maxheap, heappop_min(minheap))

    def __repr__(self):
        return f'{type(self).__name__}({self._maxheap!r}, {self._minheap!r})'
