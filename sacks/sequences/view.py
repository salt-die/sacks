from collections.abc import MutableSequence


class View(MutableSequence):
    """A mutable view of a sequence.
    """
    __slots__ = 'sequence', 'range'

    def __init__(self, sequence, range=None):
        self.sequence = sequence
        self.range = range or __builtins__['range'](len(sequence))

    def insert(self, index, item):
        """Insert item before index.
        """
        self.sequence.insert(self.range[index], item)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return View(self.sequence, self.range[key])

        return self.sequence[self.range[key]]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            r = self.range[key]
            self.sequence[r.start: r.stop: r.step] = value
        else:
            self.sequence[self.range[key]] = value

    def __delitem__(self, key):
        if isinstance(key, slice):
            r = self.range[key]
            del self.sequence[r.start: r.stop: r.step]
        else:
            del self.sequence[self.range[key]]

    def __len__(self):
        return sum(1 for _ in self)  # len(self.range) isn't exactly correct as range.end might be larger than sequence

    def __iter__(self):
        for i in self.range:
            yield self.sequence[i]

    def __reversed__(self):
        for i in reversed(self.range):
            yield self.sequence[i]

    def __repr__(self):
        return f'{type(self).__name__}(sequence={self.sequence!r}, range={self.range!r})'

    def __str__(self):
        return f'{type(self.sequence)(self)!r}'
