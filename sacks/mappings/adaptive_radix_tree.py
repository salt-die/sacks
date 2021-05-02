from collections.abc import MutableMapping

from ..primitives import RadixNode


class AdaptiveRadixTree(MutableMapping):
    def __init__(self):
        self.root = RadixNode()

