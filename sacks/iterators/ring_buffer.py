from collections.abc import Iterator, Sized

from ..primitives.sentinel import sentinel

NO_DEFAULT = sentinel("NO_DEFAULT", repr="<no default>")


class RingBuffer(Iterator, Sized):
    """A FIFO buffer with a fixed size. [https://en.wikipedia.org/wiki/Circular_buffer]
    """
    __slots__ = '_buffer', 'size', '_len', '_head',

    def __init__(self, size, iterable=()):
        self.size = size
        self._buffer = [ None ] * size
        self._len = 0
        self._head = 0
        self.extend(iterable)

    def __len__(self):
        return self._len

    def peek(self, default=NO_DEFAULT):
        """
        Return the next item without consuming it.  If default is provided and buffer
        is empty return default else raise StopIteration.
        """

        if len(self) == 0:
            if default is NO_DEFAULT:
                raise StopIteration('buffer empty')
            return default

        return self._buffer[self._head - self._len]

    def popleft(self):
        """
        Return the next item.

        Raises
        ------
        StopIteration if buffer is empty.

        """
        if self._len == 0:
            raise StopIteration('buffer empty')

        try:
            return self._buffer[self._head - self._len]
        finally:
            self._len -= 1

    __next__ = popleft

    def append(self, item):
        """
        Append `item` to the buffer.

        Raises
        ------
        MemoryError if buffer is full.

        """
        if self._len == len(self._buffer):
            raise MemoryError('buffer full')

        self._buffer[self._head] = item
        self._head = (self._head + 1) % self.size
        self._len += 1

    def extend(self, iterable):
        """Append each item of `iterable`.
        """
        for item in iterable:
            self.append(item)

    def __repr__(self):
        len_ = len(self)
        start = self._head - len_
        return f'{type(self).__name__}({", ".join(repr(self._buffer[(start + i) % self.size]) for i in range(len_))})'
