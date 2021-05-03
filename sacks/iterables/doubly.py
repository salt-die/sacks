from collections.abc import Collection, Reversible

from ..primitives import Block


class DoublyLinkedList(Collection, Reversible):
    """A doubly-linked list implementation for use with higher-order collections.  Appends return the underlying block primitives.
    """
    __slots__ = '_len', 'root',

    def __init__(self, iterable=()):
        self._len = -1
        self.root = Block(list=self)
        self.extend(iterable)

    def __iter__(self):
        current = self.root.next
        while current is not self.root:
            yield current.val
            current = current.next

    def __reversed__(self):
        current = self.root.prev
        while current is not self.root:
            yield current.val
            current = current.prev

    def __contains__(self, item):
        for element in self:
            if element == item:
                return True
        return False

    def __len__(self):
        return self._len

    def append(self, val):
        return Block(val, prev=self.root.prev, next=self.root, list=self)

    def appendleft(self, val):
        return Block(val, prev=self.root, next=self.root.next, list=self)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def extendleft(self, iterable):
        for item in iterable:
            self.appendleft(item)

    def pop(self):
        if len(self) == 0:
            raise KeyError

        return self.root.prev.pop()

    def popleft(self):
        if len(self) == 0:
            raise KeyError

        return self.root.next.pop()

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(repr(item) for item in self)})'
