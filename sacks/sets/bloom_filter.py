from collections.abc import Container
from bitarray import bitarray


class BloomFilter(Container):
    """A memory-efficient data structure with probabalistic membership checks.
    """
    __slots__ = '_bitarray', '_nhashes',

    def __init__(self, iterable=(), / , size=2**16, hashes=2**3):
        self._bitarray = bitarray(size)
        self._bitarray[:] = 0

        self._nhashes = hashes

        self |= iterable

    def _hash(self, item, i):
        return hash((item, i)) % len(self._bitarray)

    def __contains__(self, item):
        return all(self._bitarray[self._hash(item, i)] for i in range(self._nhashes))

    def add(self, item):
        for i in range(self._nhashes):
            self._bitarray[self._hash(item, i)] = 1

    def __ior__(self, iterable):
        for item in iterable:
            self.add(item)
        return self

    def update(self, *others):
        for other in others:
            self |= other

    def isdisjoint(self, iterable):
        return all(item not in self for item in iterable)

    def issuperset(self, iterable):
        return all(item in self for item in iterable)

    def intersects(self, iterable):
        return any(item in self for item in iterable)

    def __repr__(self):
        bits = self._bitarray
        size = len(bits)
        return f'{type(self).__name__}(size={size}, nhashes={self._nhashes})[{bits.count() / size}]'
