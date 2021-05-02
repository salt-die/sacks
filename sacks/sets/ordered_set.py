from collections.abc import MutableSet

from ..iterables import DoublyLinkedList


class OrderedSet(MutableSet):
    """An ordered set.
    """
    __slots__ = '_item_map', '_item_seq',

    def __init__(self, iterable=()):
        self._item_map = { }
        self._item_seq = DoublyLinkedList()

        self |= iterable

    def __contains__(self, item):
        return item in self._item_map

    def __iter__(self):
        return iter(self._item_seq)

    def __reversed__(self):
        return reversed(self._item_seq)

    def __len__(self):
        return len(self._item_map)

    def add(self, item):
        if item not in self._item_map:
            self._item_map[item] = self._item_seq.append(item)

    def discard(self, item):
        if item in self:
            self._item_map.pop(item).pop()

    def pop(self):
        item = self._item_seq.pop()
        del self._item_map[item]
        return item

    def popleft(self):
        item = self._item_seq.popleft()
        del self._item_map[item]
        return item

    def __repr__(self):
        return f'{type(self).__name__}({{{", ".join(map(repr, self))}}})'
