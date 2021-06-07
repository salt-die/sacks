from collections import defaultdict
from collections.abc import MutableSet


class MultiSetch(MutableSet):
    """
    A multiset with choice.

    Exposes a sequence of the items of the set, `as_sequence`, that one can use with the
    `random` module's `choice`, `choices`, and `sample` functions. This sequence is efficiently
    maintained (though order is not maintained) as the multiset is mutated.

    """
    __slots__ = '_item_map', 'as_sequence',

    def __init__(self, iterable=()):
        self._item_map = defaultdict(set)
        self.as_sequence = [ ]

        self |= iterable

    def __contains__(self, item):
        return item in self._item_map

    def __iter__(self):
        return iter(self.as_sequence)

    def __len__(self):
        return len(self.as_sequence)

    def add(self, item):
        self._item_map[item].add(len(self.as_sequence))
        self.as_sequence.append(item)

    def discard(self, item):
        item_map = self._item_map

        if item not in item_map:
            return

        new_pos = item_map[item].pop()

        if not item_map[item]:
            del item_map[item]

        items = self.as_sequence
        last_item = items.pop()

        if new_pos != (old_pos := len(items)):
            item_map[last_item].remove(old_pos)
            item_map[last_item].add(new_pos)
            items[new_pos] = last_item

    def clear(self):
        self._item_map.clear()
        self.as_sequence.clear()

    def __repr__(self):
        return f'{type(self).__name__}({{{", ".join(map(repr, self))}}})'
