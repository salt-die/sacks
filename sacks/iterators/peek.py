from collections.abc import Iterator

from ..iterables import DoublyLinkedList

RAISE = object()


class Peek(Iterator):
    """An iterator-wrapper that allows one to peek at the next items without consuming them.
    """
    __slots__ = 'iterable', '_peeked',

    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self._peeked = DoublyLinkedList()

    def __next__(self):
        if self._peeked:
            return self._peeked.popleft()

        return next(self.iterable)

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False

        return True

    def peek(self, n=1, default=RAISE):
        """
        For `n == 1`, returns the next item without consuming it.

        For `n > 1`, returns the next n items (as a tuple) without consuming them.

        Provide a `default` value to suppress StopIteration.

        Raises
        ------
        StopIteration if `n` larger than items left in iterable and no default provided.
        """
        peeked = self._peeked

        try:
            while len(peeked) < n:
                peeked.append(next(self.iterable))

        except StopIteration:
            if default is RAISE:
                raise

            if n == 1:
                return default

            return *peeked, *(default for _ in range(n - len(peeked)))

        it = iter(peeked)
        if n == 1:
            return next(it)
        return tuple(next(it) for _ in range(n))

    def __repr__(self):
        return f'{type(self).__name__}({self.iterable!r})'

    def __str__(self):
        try:
            self.peek(4)
        except StopIteration:
            items = ", ".join(map(str, self._peeked))
        else:
            items = ', '.join(map(str, self.peek(3))) + ', ...'

        return f'{type(self).__name__}([{items}])'
