from collections.abc import MutableSequence
from functools import wraps


class InvalidatedView(Exception):
    ...


def raise_if_invalidated(cls):
    """Adds a validation check to all methods of `View`.
    """
    def check(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if len(self.sequence) != self._olen:
                raise InvalidatedView("sequence length changed")
            return func(self, *args, **kwargs)
        return wrapper

    for key, method in cls.__dict__.items():
        if key != '__init__' and callable(method):
            setattr(cls, key, check(method))

    return cls


@raise_if_invalidated
class View(MutableSequence):
    """
    A mutable view of a sequence.

    Warning
    -------
    Passing in a `_range` is not recommended.  Better to slice a default `View` instead.

    Raises
    ------
    `InvalidatedView` if the underlying sequence's length changes.
    """
    __slots__ = 'sequence', '_olen', '_range',

    def __init__(self, sequence, _range=None):
        self.sequence = sequence
        self._olen = len(sequence)  # original length
        self._range = _range or range(self._olen)

    def insert(self, index, item):
        """Insert item before index.
        """
        self.sequence.insert(self._range[index], item)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return View(self.sequence, self._range[key])

        return self.sequence[self._range[key]]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            r = self._range[key]
            self.sequence[r.start: r.stop: r.step] = value
        else:
            self.sequence[self._range[key]] = value

    def __delitem__(self, key):
        if isinstance(key, slice):
            r = self._range[key]
            del self.sequence[r.start: r.stop: r.step]
        else:
            del self.sequence[self._range[key]]

    def __len__(self):
        return len(self._range)

    def __iter__(self):
        for i in self._range:
            yield self.sequence[i]

    def __reversed__(self):
        for i in reversed(self._range):
            yield self.sequence[i]

    def __repr__(self):
        return f'{type(self).__name__}(sequence={self.sequence!r}, _range={self._range!r})'

    def __str__(self):
        return f'{type(self.sequence)(self)!r}'
