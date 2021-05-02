from collections.abc import MutableMapping

from ..primitives import RadixNode


class AdaptiveRadixTree(MutableMapping):
    __slots__ = 'root',

    def __init__(self):
        self.root = RadixNode()

