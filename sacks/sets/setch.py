from collections.abc import MutableSet


class Setch(MutableSet):
    """
    Set with choice.  Setch.

    Exposes a sequence of the items of this set, `as_sequence`, that one can use with the
    `random` module's `choice`, `choices`, and `sample` functions. This sequence is efficiently
    maintained (though order is not maintained) as the set is mutated.
    """
    __slots__ = '_item_map', 'as_sequence'

    def __init__(self, iterable=None):
        self._item_map = { }
        self.as_sequence = [ ]

        if iterable:
            self |= iterable

    def __contains__(self, item):
        return item in self._item_map

    def __iter__(self):
        return iter(self._item_map)

    def __len__(self):
        return len(self._item_map)

    def add(self, item):
        if item not in self:
            self._item_map[item] = len(self.as_sequence)
            self.as_sequence.append(item)

    def discard(self, item):
        if item not in self:
            return

        position = self._item_map.pop(item)
        last_item = self.as_sequence.pop()
        if item != last_item:
            self.as_sequence[position] = last_item
            self._item_map[last_item] = position

    def clear(self):
        self._item_map.clear()
        self.as_sequence.clear()

    def __repr__(self):
        return f'{type(self).__name__}({{{", ".join(map(repr, self))}}})'
