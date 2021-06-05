from abc import ABC, abstractmethod
from collections.abc import Sized
from functools import wraps

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
    __slots__ = '_size', '_root',

    def __init__(self, iterable=()):
        self._root = None
        self._size = 0

        for item in iterable:
            self.heappush(item)

    @property
    def root(self):
        return self._root

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

        return self._root.key


class DeletedEntryError(Exception):
    ...


class Entry:
    """An interface for decreasing/deleting a key in a heap. (Tree nodes will stay private.)
    """
    __slots__ = '_node', '_heap',

    def __init__(self, node, heap):
        self._node = node
        self._heap = heap

    @property
    def is_deleted(self):
        return not hasattr(self, '_node') or not self._node.next

    @property
    def key(self):
        if self.is_deleted:
            raise DeletedEntryError

        return self._node.key

    def decrease_key(self, key):
        if self.is_deleted:
            raise DeletedEntryError

        if key > self.key:
            raise keyError(f'{key} greater than {self.key}')

        self._heap.decrease_key(self._node, key)

    def delete(self):
        if self.is_deleted:
            raise DeletedEntryError

        self.decrease_key(NEG_INF)
        self._heap.heappop()
        del self._node
        del self._heap

    def __repr__(self):
        key = 'DELETED' if self.is_deleted else repr(self.key)
        return f'{type(self).__name__}({key})'
