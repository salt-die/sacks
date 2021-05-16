from collections.abc import MutableSet
from ..primitives import SkipListBlock


class SkipList(MutableSequence):
    """
    An ordered sequence with O(log n) search and insertion.

    Parameters
    ----------
    p:
        Probability a block is linked on the next level. (default: .5)
    """
    __slots__ = '_level', '_head', '_tail', '_path', '_resize_len', '_len',

    def __init__(self, iterable=(), *, p=.5):
        self._level = 0
        self._len = 0
        self._resize_len = 1

        self.p = p

        self._head = SkipListBlock(None)
        self._tail = SkipListBlock(None)
        self._head.skip = self._tail.skip = 0
        self._head.forwards.append(self._tail)

    def _random_level(self):
        level = 1
        while level < self._level and random() < self.p:
            level += 1
        return level

    def __len__(self):
        return self._len

    def _path_to(self, block):
        """Generate a path of blocks through the skip list.
        """
        node = self._head
        skip = 0
        for i in reversed(range(node.height)):
            next_node = node.forwards[i]
            while next_node is not self._tail and next_node < block:
                node, next_node = next_node, next_node.forwards[i]
                skip += node.skip
            yield node, skip

    def add(self, item):
        self._len += 1
        if self._len >= self._resize_len:
            self._level += 1
            self._head.forwards.append(self._tail)
            self._tail.skip = len(self)
            self._resize_len = round((1 / self.p) ** self._level)

        block = SkipListBlock(item, self._random_level())

    def discard(self, item):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def contains(self, item):
        raise NotImplementedError