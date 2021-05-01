from collections.abc import Reversible

from ..primitives import Block


class DoublyLinkedList(Reversible):
    """A doubly-linked list implementation for use with higher-order collections.  Appends return the underlying block primitives.
    """
    __slots__ = 'root'

    def __init__(self, iterable=()):
        self.root = Block()
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

    def append(self, val):
        return Block(val, prev=self.root.prev, next=self.root)

    def appendleft(self, val):
        return Block(val, prev=self.root, next=self.root.next)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def extendleft(self, iterable):
        for item in iterable:
            self.appendleft(item)

    def pop(self):
        if self.root.prev is self.root:
            raise KeyError

        return self.root.prev.pop()

    def popleft(self):
        if self.root.next is self.root:
            raise KeyError

        return self.root.next.pop()

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(repr(item) for item in self)})'
