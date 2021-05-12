from collections.abc import Container, Reversible

from ..primitives import Block


class DoublyLinkedList(Container, Reversible):
    """
    A doubly-linked list implementation for use with higher-order collections.

    Notes
    -----
    Appends return the underlying block primitives for structures that may want access to them.

    """
    __slots__ = 'root',

    def __init__(self, iterable=()):
        self.root = Block()
        self.extend(iterable)

    def __iter__(self):
        current = self.root.next
        while current is not self.root:
            yield current.value
            current = current.next

    def __reversed__(self):
        current = self.root.prev
        while current is not self.root:
            yield current.value
            current = current.prev

    def __contains__(self, item):
        for element in self:
            if element == item:
                return True
        return False

    def __bool__(self):
        return self.root is not self.root.next

    def append(self, value):
        return Block(value, prev=self.root.prev, next=self.root)

    def appendleft(self, value):
        return Block(value, prev=self.root, next=self.root.next)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def extendleft(self, iterable):
        for item in iterable:
            self.appendleft(item)

    def pop(self):
        if not self:
            raise IndexError('pop from empty list')

        return self.root.prev.pop()

    def popleft(self):
        if not self:
            raise IndexError('pop from empty list')

        return self.root.next.pop()

    def rotate(self):
        """Rotate this deque 1 step to the right.
        """
        root = self.root

        root.remove()
        root.next = root.prev
        root.prev = root.prev.prev
        root.insert()

    def __del__(self):
        self.root.pop()  # Remove root's circular reference

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(repr(item) for item in self)}])'
