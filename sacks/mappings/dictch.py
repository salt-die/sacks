from collections.abc import MutableMapping
from ..sets import Setch


class Dictch(MutableMapping):
    """
    A dict with choice.

    Exposes a sequence of the keys of this mapping, `as_sequence`, that one can use with the
    `random` module's `choice`, `choices`, and `sample` functions. This sequence is efficiently
    maintained (though order is not maintained) as the dict is mutated.
    """
    __slots__ = '_items', '_setch',

    def __init__(self, *args, **kwargs):
        self._items = { }
        self._setch = Setch()

        for key, value in args:
            self[key] = value
        self.update(kwargs)

    @property
    def as_sequence(self):
        return self._setch.as_sequence

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value
        self._setch.add(key)

    def __delitem__(self, key):
        del self._items[key]
        self._setch.discard(key)

    def __repr__(self):
        return f'{type(self).__name__}({self._items!r})'
