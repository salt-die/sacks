from collections.abc import MutableMapping

from ..primitives.radix_node import RadixNode


class AdaptiveRadixTree(MutableMapping):
    """
    A memory-efficient trie in which each node that is the only child is merged with its parent.
    [https://en.wikipedia.org/wiki/Radix_tree]

    Parameters
    ----------
    type : sliceable sequence-type comparable with `<` and joinable with `+`. (keyword-only, default: str)

    """
    __slots__ = '_root', '_type', '_len',

    def __init__(self, *args, type=str, **kwargs):
        self._root = RadixNode(type())
        self._type = type
        self._len = 0

        self |= dict(*args, **kwargs)

    @property
    def root(self):
        return self._root

    def __getitem__(self, item):
        try:
            return self._root.find(item)
        except KeyError:
            raise KeyError(item) from None

    def __setitem__(self, key, value):
        if not isinstance(key, self._type):
            raise TypeError(f'{type(key).__name__} is not {self._type.__name__}')

        self._len += self._root.add(key, value)

    def __delitem__(self, key):
        try:
            self._root.delete(key)
        except KeyError:
            raise KeyError(key) from None
        else:
            self._len -= 1

    def __ior__(self, other):
        self.update(other)
        return self

    def __iter__(self):
        yield from self._root.iter_keys()

    keys = __iter__

    def values(self):
        yield from self._root.iter_datas()

    def items(self):
        yield from self._root.iter_items()

    def __len__(self):
        return self._len

    def __repr__(self):
        items = ', '.join(f'{key!r}: {value!r}' for key, value in self.items())
        return f'{type(self).__name__}(type={self._type.__name__}, **{{{items}}})'

    def __str__(self):
        return str(self._root)
