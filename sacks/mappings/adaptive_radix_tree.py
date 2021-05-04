from collections.abc import MutableMapping

from ..primitives import RadixNode


class AdaptiveRadixTree(MutableMapping):
    """
    A memory-efficient trie in which each node that is the only child is merged with its parent.
    [https://en.wikipedia.org/wiki/Radix_tree]

    Parameters
    ----------
    type : sliceable sequence-type comparable with `<` and joinable with `+`. (keyword-only, default: str)

    """
    __slots__ = '_root', '_type', '_len',

    def __init__(self, *items, type=str, **kwargs):
        self._root = RadixNode(type())
        self._type = type
        self._len = 0

        for key, value in items:
            self[key] = value
        self |= kwargs

    def __getitem__(self, item):
        try:
            return self._root.find(RadixNode(item))
        except KeyError as e:
            raise KeyError(item) from e

    def __setitem__(self, item, value):
        if not isinstance(item, self._type):
            raise TypeError(f'{type(item).__name__} is not {self._type.__name__}')
        self._len += self._root.add(RadixNode(item, data=value))

    def __delitem__(self, item):
        if item == self._root.prefix:
            # Special case for the root (node deletions are expected
            # to be from parents of the node, but the root has no parents).
            # Note the root won't be removed, but its data may be erased.
            if self._root.is_key:
                self.root.data = RadixNode.NOT_KEY
                self._len -= 1
                return
            raise KeyError(item)

        try:
            self._root.delete(RadixNode(item))
        except KeyError as e:
            raise KeyError(item) from e
        else:
            self._len -= 1

    def __ior__(self, other):
        self.update(other)
        return self

    def __iter__(self):
        yield from self._root.iter_keys()

    def __len__(self):
        return self._len

    def __repr__(self):
        items = ', '.join(f'{key!r}: {self[key]!r}' for key in self)
        return f'{type(self).__name__}(type={self._type.__name__}, {{{items}}})'

    def __str__(self):
        return str(self._root)
