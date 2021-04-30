class Necklace:
    """
    `Necklace`s are immutable sequences that "wrap-around".

    Because `Necklaces` wrap, `__getitem__` slices will also wrap.

    Notes
    -----
    To facilitate fast equality comparisons, `Necklace`s store their canonical form (specifically, the least shift).

    Example
    -------
    ```
    >>> n = Necklace((1, 2, 3, 0)); m = Necklace((3, 0, 1, 2))
    >>> n == m
    True
    >>> n[-3: 15: 2]
    (2, 0, 2, 0, 2, 0, 2, 0, 2)
    ```
    """
    __slots__ = '_items', 'least_shift'

    def __new__(cls, iterable):
        items = tuple(iterable)
        least_shift = min(items[i:] + items[:i] for i in range(len(items)))

        necklace = super().__new__(cls)
        super().__setattr__(necklace, '_items', items)
        super().__setattr__(necklace, 'least_shift', least_shift)
        return necklace

    def __setattr__(self, attr, value):
        raise AttributeError("can't set attribute")

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.least_shift == other.least_shift

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, key):
        if isinstance(key, slice):
            return tuple(self._items[i % len(self)] for i in range(key.start or 0, key.stop or len(self), key.step or 1))
        else:
            return self._items[key % len(self)]

    def __repr__(self):
        return f'{type(self).__name__}{self._items!r}'
