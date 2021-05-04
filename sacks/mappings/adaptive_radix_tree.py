from collections.abc import MutableMapping

from ..primitives import RadixNode


class AdaptiveRadixTree(MutableMapping):
    """
    A memory-efficient trie in which each node that is the only child is merged with its parent.
    [https://en.wikipedia.org/wiki/Radix_tree]

    Parameters
    ----------
    type : sequence-type comparable with `<` and joinable with `+`. (keyword-only, default: str)

    """
    __slots__ = 'root', '_len',

    def __init__(self, *items, type=str, **kwargs):
        self.root = RadixNode(type())
        self._len = 0

        for key, value in items:
            self[key] = value
        self |= kwargs

    def __getitem__(self, item):
        try:
            return self.root.find(RadixNode(item))
        except KeyError as e:
            raise KeyError(item) from e

    def __setitem__(self, item, value):
        self._len += self.root.add(RadixNode(item, data=value))

    def __delitem__(self, item):
        try:
            self.root.delete(RadixNode(item))
        except KeyError as e:
            raise KeyError(item) from e
        else:
            self._len -= 1

    def __ior__(self, other):
        self.update(other)
        return self

    def __iter__(self):
        yield from self.root.iter_keys()

    def __len__(self):
        return self._len

    def __repr__(self):
        items = ', '.join(f'{key!r}: {self[key]!r}' for key in self)
        return f'{type(self).__name__}({{{items}}})'

    def __str__(self):
        return str(self.root)
