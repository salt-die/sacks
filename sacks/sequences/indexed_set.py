from collections.abc import MutableSet, Sequence


class IndexedSet(MutableSet, Sequence):  # We can't inherit MutableSequence as there is no reasonable implementation of `__setitem__` or `insert`
    """
    An indexable set.

    Notes
    -----
    Removals are O(n) and we make no attempt to micro-optimize them.  Perhaps consider `OrderedSet` instead if you want O(1) removals.
    """
    def __init__(self, iterable):
        self._items = set( )
        self._item_seq = [ ]

        for item in iterable:
            self.add(item)

    def count(self, item):  # Silly, but still a better version than mix-in
        return int(item in self)

    def clear(self):
        """Remove all elements from this set.
        """
        self._items.clear()
        self._item_seq.clear()

    def pop(self):
        """Remove and return the last item in the set.
        """
        item = self._item_seq.pop()
        self._items.remove(item)
        return item

    def discard(self, item):
        """
        Remove an item from the set if it's in the set.
        """
        if item in self:
            self._items.remove(item)
            self._item_seq.remove(item)

    def add(self, item):
        """Add an item to the set.
        """
        if item not in self._items:
            self._items.add(item)
            self._item_seq.append(item)

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._item_seq)

    def __getitem__(self, key):
        return self._item_seq[key]

    def __delitem__(self, key):
        self.remove(self[key])

    def __repr__(self):
        return f'{type(self).__name__}({self._item_seq!r})'
