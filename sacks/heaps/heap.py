from abc import ABC, abstractmethod
from collections.abc import Sized

from ..primitives import sentinel

NEG_INF = sentinel(
    name='NegInf',
    repr='NEG_INF',
    methods={
        '__lt__': lambda self, other: True,
        '__gt__': lambda self, other: False,
    },
)


class Heap(ABC, Sized):
    __slots__ = '_size', 'root',

    def __len__(self):
        return self._size

    @abstractmethod
    def heappop(self):
        """Pop the smallest item off the heap, maintaining the heap invariant.
        """
        pass

    @abstractmethod
    def heappush(self, value):
        """Push item onto heap, maintaining the heap invariant.
        """
        pass

    def min(self):
        if not self:
            raise IndexError('empty heap')

        return self.root.value


class Entry:
    """An interface for decreasing/deleting a key in a heap. (Tree nodes will stay private.)
    """
    __slots__ = '_node', '_heap',

    def __init__(self, node, heap):
        self._node = node
        self._heap = heap

    @property
    def value(self):
        return self._node.value

    def decrease_key(self, value):
        if value >= self.value:
            raise ValueError(f'{value} greater than {self.value}')

        self._heap.decrease_key(self._node, value)

    def delete(self):
        self.decrease_key(NEG_INF)
        self._heap.heappop()

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'
