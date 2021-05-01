from collections import deque
from collections.abc import Iterator


class Peek(Iterator):
    """
    An iterator-wrapper that allows one to peek at the next items without consuming them.
    """
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self._peeked = deque()

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

    def peek(self, n=1):
        """
        For `n == 1`, returns the next item without consuming it.

        For `n > 1`, returns the next n items (as a tuple) without consuming them.

        Raises StopIteration
        """
        while len(self._peeked) < n:
            self._peeked.append(next(self.iterable))

        if n == 1:
            return self._peeked[0]

        return tuple(self._peeked[i] for i in range(n))

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
