from collections.abc import MutableSequence

from ..primitives import RopeInternal, RopeLeaf


class Rope(MutableSequence):
    """A tree-like structure that allows efficient manipulation of variable-length types.
    """
    def __init__(self, iterable, *, leafsize=8):
        ...

    def __getitem__(self, key):
        ...

    def __len__(self):
        ...