from collections.abc import Iterator, Sized


class RingBuffer(Iterator, Sized):
    """A FIFO buffer with a fixed size. [https://en.wikipedia.org/wiki/Circular_buffer]
    """
    __slots__ = '_buffer', 'size', '_len', '_head',

    def __init__(self, size, iterable=()):
        self.size = size
        self._buffer = [None] * size
        self._len = 0
        self._head = 0
        self.write_from(iterable)

    def __len__(self):
        return self._len

    def read(self):
        """
        Read the next item.

        Raises
        ------
        StopIteration if buffer is empty.

        """
        if self._len == 0:
            raise StopIteration("buffer empty")

        self._len -= 1

        return self._buffer[self._head - self._len + 1]

    __next__ = read

    def write(self, item):
        """
        Write `item` to the buffer.

        Raises
        ------
        MemoryError if buffer is full.

        """
        if self._len == len(self._buffer):
            raise MemoryError("buffer full")

        self._buffer[self._head] = item
        self._head = (self._head + 1) % self.size
        self._len += 1
        return self._len

    def write_from(self, iterable):
        """Writes each item of `iterable`.
        """
        for item in iterable:
            self.write(item)
        return self._len

    def __repr__(self):
        len_ = len(self)
        start = self._head - len_
        return f'{type(self).__name__}({", ".join(repr(self._buffer[(start + i) % self.size]) for i in range(len_))})'
