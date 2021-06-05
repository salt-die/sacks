from collections.abc import Sequence


class Column(Sequence):
    """A immutable view of the `i`th entry of each sequence in a sequence of sequences.
    """
    __slots__ = '_i', '_sequences'

    def __init__(self, i, sequences):
        self._i = i
        self._sequences = sequences

    @property
    def i(self):
        return self._i

    def __getitem__(self, i):
        return self._sequences[i][self._i]

    def __len__(self):
        return len(self._sequences)

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}])'
