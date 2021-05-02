from collections.abc import MutableMapping


class Bijection(MutableMapping):
    """
    A one-to-one mapping.

    `reverse` method will swap maps to allow reverse lookup.
    """
    __slots__ = '_map', '_reverse_map',

    def __init__(self, *args, **kwargs):
        self._map = { }
        self._reverse_map = { }

        for key, value in args:
            self[key] = value
        self.update(kwargs)

    def __contains__(self, item):
        return item in self._map

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        return iter(self._map)

    def __getitem__(self, key):
        return self._map[key]

    def __setitem__(self, key, value):
        reverse = self._reverse_map

        if value in reverse:
            raise ValueError(f"{reverse[value]} already mapped to {value}")

        if key in self:
            del reverse[self[key]]

        self._map[key] = value
        reverse[value] = key

    def __delitem__(self, key):
        del self._reverse_map[self._map.pop(key)]

    def __repr__(self):
        return f'{type(self).__name__}({self._map!r})'

    def reverse(self):
        self._reverse_map, self._map = self._map, self._reverse_map
