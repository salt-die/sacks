from collections.abc import Container, Reversible

from ..primitives.block import Block


class DoublyLinkedList(Container, Reversible):
    """
    A doubly-linked list implementation for use with higher-order collections.

    Notes
    -----
    Appends return the underlying block primitives for structures that may want access to them.

    """
    __slots__ = '_root',

    def __init__(self, iterable=()):
        self._root = Block()
        self.extend(iterable)

    @property
    def root(self):
        return self._root

    def __iter__(self):
        current = self._root
        while (current := current.next) is not self._root:
            yield current.value

    def __reversed__(self):
        current = self._root.prev
        while current is not self._root:
            yield current.value
            current = current.prev

    def __contains__(self, item):
        for element in self:
            if element == item:
                return True
        return False

    def __bool__(self):
        return self._root is not self._root.next

    def append(self, value):
        return Block(value, prev=self._root.prev, next=self._root)

    def appendleft(self, value):
        return Block(value, prev=self._root, next=self._root.next)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def extendleft(self, iterable):
        for item in iterable:
            self.appendleft(item)

    def pop(self):
        if not self:
            raise IndexError('pop from empty list')

        return self._root.prev.pop()

    def popleft(self):
        if not self:
            raise IndexError('pop from empty list')

        return self._root.next.pop()

    def rotate(self):
        """Rotate this deque 1 step to the right.
        """
        root = self._root

        root.remove()
        root.next = root.prev
        root.prev = root.prev.prev
        root.insert()

    def __del__(self):
        self._root.pop()  # Remove root's circular reference

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(repr(item) for item in self)}])'
