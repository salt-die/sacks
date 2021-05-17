from collections.abc import MutableSet
from random import random

from ..primitives import SkipListBlock
from ..primitives._sentinel import sentinel

TAIL = sentinel('Tail', repr='TAIL', methods={ '__le__': lambda self, other: False })


class SkipList(MutableSet):
    """
    An ordered sequence with O(log n) search and insertion.

    Parameters
    ----------
    p:
        Probability a block is linked on the next level. (default: .5)
    """
    __slots__ = '_len', 'p', '_head',

    def __init__(self, iterable=(), *, p=.5):
        self._len = 0
        self._head = SkipListBlock('HEAD', [ TAIL ], [ 1 ])
        self.p = p

    @property
    def max_level(self):
        return len(self._head.forward_links)

    def __len__(self):
        return self._len

    def _random_level(self):
        level = 1
        while random() < self.p:
            level += 1
        return level

    def add(self, item):
        self._len += 1

        levels = self._random_level()
        new_block = SkipListBlock(item, [ None ] * levels, [ None ] * levels)

        # Add new levels to self._head if needed.
        if levels > self.max_level:
            new_levels = levels - self.max_level
            self._head.forward_links.extend(TAIL for _ in range(new_levels))
            self._head.skips.extend(self._len for _ in range(new_levels))

        # Create a path through the skip list to new_block.
        path = [ None ] * self.max_level
        skips = [ 0 ] * self.max_level
        node = self._head
        for level in reversed(range(self.max_level)):
            while node.forward_links[level] <= new_block:
                skips[level] += node.skips[level]
                node = node.forward_links[level]
            path[level] = node

        # Update pointers and skips.
        total_skip = 0
        for level in range(levels):
            previous = path[level]
            # Pointers
            new_block.forward_links[level] = previous.forward_links[level]
            previous.forward_links[level] = new_block
            # Skips
            new_block.skips[level] = previous.skips[level] - total_skip
            previous.skips[level] = total_skip + 1
            total_skip += skips[level]

        # More skips.
        for level in range(levels, self.max_level):
            path[level].skips[level] += 1

    def discard(self, item):
        raise NotImplementedError

    def __iter__(self):
        current = self._head.forward_links[0]
        while current is not TAIL:
            yield current.value
            current = current.forward_links[0]

    def __contains__(self, item):
        raise NotImplementedError

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}], p={self.p})'

    def _iter_blocks(self, level):
        SPACING = 5

        yield f'HEAD{"-" * (SPACING + 2) * (self._head.skips[level] - 1)}->'

        current = self._head.forward_links[level]
        while current is not TAIL:
            yield f'{current.value!r:^{SPACING}}{"-" * (SPACING + 2) * (current.skips[level] - 1)}->'
            current = current.forward_links[level]

        yield f'TAIL'

    def __str__(self):
        return '\n'.join(''.join(self._iter_blocks(level)) for level in reversed(range(self.max_level)))
