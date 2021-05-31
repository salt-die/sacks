from abc import ABC, abstractmethod
from collections.abc import Sized

from ..primitives.sentinel import sentinel

NEG_INF = sentinel(
    name='NegInf',
    repr='NEG_INF',
    methods={
        '__lt__': lambda self, other: True,
        '__le__': lambda self, other: True,
        '__gt__': lambda self, other: False,
        '__ge__': lambda self, other: False,
    },
)


class Heap(ABC, Sized):
    __slots__ = '_size', 'root',

    def __init__(self, iterable=()):
        self.root = None
        self._size = 0

        for item in iterable:
            self.heappush(item)

    def __len__(self):
        return self._size

    @abstractmethod
    def heappop(self):
        """Pop the smallest item off the heap, maintaining the heap invariant.
        """
        pass

    @abstractmethod
    def heappush(self, key):
        """Push item onto heap, maintaining the heap invariant.
        """
        pass

    @property
    def min(self):
        if not self:
            raise IndexError('empty heap')

        return self.root.key


class Entry:
    """An interface for decreasing/deleting a key in a heap. (Tree nodes will stay private.)
    """
    __slots__ = '_node', '_heap',

    def __init__(self, node, heap):
        self._node = node
        self._heap = heap

    @property
    def key(self):
        return self._node.key

    def decrease_key(self, key):
        if key >= self.key:
            raise keyError(f'{key} greater than {self.key}')

        self._heap.decrease_key(self._node, key)

    def delete(self):
        self.decrease_key(NEG_INF)
        self._heap.heappop()
        del self._node
        del self._heap

    def __repr__(self):
        if not hasattr(self, '_node'):
            return f'{type(self).__name__}(DELETED)'
        return f'{type(self).__name__}({self.key!r})'
