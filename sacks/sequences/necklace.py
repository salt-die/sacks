from collections.abc import Sequence


class Necklace(Sequence):
    """
    An immutable sequence that "wraps-around". [https://en.wikipedia.org/wiki/Necklace_(combinatorics)]

    Because `Necklace`s wrap, `__getitem__` slices will also wrap.

    Notes
    -----
    To facilitate fast equality comparisons, `Necklace`s store their canonical form in the attribute `least_shift`.

    Example
    -------
    ```
    >>> n = Necklace((1, 2, 3, 0)); m = Necklace((3, 0, 1, 2))
    >>> n == m
    True
    >>> n[-3: 15: 2]
    (2, 0, 2, 0, 2, 0, 2, 0, 2)
    ```
    Note that despite equality of `n` and `m`, their indexing won't be equal.

    """
    __slots__ = '_items', 'least_shift', 'aperiodic',

    def __new__(cls, iterable=()):
        items = tuple(iterable)
        shifts = set(items[i:] + items[:i] for i in range(len(items)))

        necklace = super().__new__(cls)
        super().__setattr__(necklace, '_items', items)
        super().__setattr__(necklace, 'least_shift', min(shifts))
        super().__setattr__(necklace, 'aperiodic', len(shifts) == len(items))
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
        l = len(self)
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = l if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            return tuple(self._items[i % l] for i in range(start, stop, step))
        else:
            return self._items[key % l]

    def __repr__(self):
        return f'{type(self).__name__}{self._items!r}'
