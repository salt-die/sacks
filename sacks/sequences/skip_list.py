from collections.abc import MutableSet
from ..primitives import SkipListBlock

P = .5

def random_level(max_level):
        level = 1
        while random() < P and level < max_level:
            level += 1
        return level


class SkipList(MutableSequence):
    """An ordered sequence with O(log n) search and insertion.
    """
    __slots__ = 'head', 'levels', '_resize_len', '_len',

    def __init__(self, iterable=()):
        self.head = SkipListBlock(None)

        self.levels = 0
        self._resize_len = 1
        self._len = 0

    def __len__(self):
        return self._len

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, value):
        self._len = value
        self._resize()

    def _resize(self):
        if self._len >= self._resize_len:
            self.levels += 1
            self._resize_len = int((1 / P) ** self.levels)

    def __iter__(self):
        raise NotImplementedError

    def contains(self, item):
        raise NotImplementedError

    def add(self, item):
        raise NotImplementedError
        #     self.countdown -= 1
        #     self._len += 1

        #     next_block = self.head
        #     while True:
        #         for level in next_block.forwards:
        #             if level.value < item:
        #                 next_block = level

    def discard(self, item):
        raise NotImplementedError
