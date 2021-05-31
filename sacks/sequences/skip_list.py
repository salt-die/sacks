from collections.abc import MutableSet
from random import random

from ..primitives.sentinel import sentinel
from ..primitives.skip_list_block import SkipListBlock

TAIL = sentinel('Tail', repr='TAIL', methods={
    '__lt__': lambda self, other: False,
    '__le__': lambda self, other: False,
})


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
        self._head = SkipListBlock(object(), [ TAIL ], [ 1 ])
        self.p = p

        self.update(iterable)

    @property
    def max_level(self):
        return len(self._head.forward_links)

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        """
        Notes
        -----
        Slices return a list of values.

        """
        if isinstance(index, int):
            if index < -len(self) or index >= len(self):
                raise IndexError(f'index {index} out of range')

            if index < 0:
                index += len(self)

            current = self._head
            index += 1
            for level in reversed(range(self.max_level)):
                while current.skips[level] <= index:
                    index -= current.skips[level]
                    current = current.forward_links[level]
            return current.value

        start, stop, step = index.indices(self._len)
        current = self._head
        index = start + 1
        for level in reversed(range(self.max_level)):
            while current.skips[level] <= index:
                index -= current.skips[level]
                current = current.forward_links[level]

        values = [ ]
        while start < stop:
            values.append(current.value)
            for _ in range(step):
                start += 1
                current = current.forward_links[0]
                if current is TAIL:
                    return values

        return values

    def _random_level(self):
        """
        Return a random level for a block.

        Notes
        -----
        New levels are added as needed to accommodate too-large random levels.

        """
        level = 1
        while random() < self.p:
            level += 1

        # Add new levels if needed.
        if level > self.max_level:
            new_levels = level - self.max_level
            self._head.forward_links.extend(TAIL for _ in range(new_levels))
            self._head.skips.extend(self._len + 1 for _ in range(new_levels))

        return level

    def __contains__(self, item):
        current = self._head
        for level in reversed(range(self.max_level)):
            while (next_block := current.forward_links[level]) < item:
                current = next_block

        return current.forward_links[0] == item

    def add(self, item):
        random_level = self._random_level()
        new_block = SkipListBlock(item, [ None ] * random_level, [ None ] * random_level)

        # Create a path to new_block.
        path = [ None ] * self.max_level
        skips = [ 0 ] * self.max_level
        current = self._head
        for level in reversed(range(self.max_level)):
            while (next_block := current.forward_links[level]) <= new_block:
                skips[level] += current.skips[level]
                current = next_block
            path[level] = current

        # Update pointers and skips.
        total_skip = 0
        for level in range(random_level):
            previous = path[level]
            # Pointers
            new_block.forward_links[level] = previous.forward_links[level]
            previous.forward_links[level] = new_block
            # Skips
            new_block.skips[level] = previous.skips[level] - total_skip
            previous.skips[level] = total_skip + 1
            total_skip += skips[level]

        # More skips.
        for level in range(random_level, self.max_level):
            path[level].skips[level] += 1

        self._len += 1

    def update(self, *iterables):
        """Add each element in each iterable.
        """
        for iterable in iterables:
            for item in iterable:
                self.add(item)

    def remove(self, item):
        # Create a path through to block that contains item.
        path = [ None ] * self.max_level
        current = self._head
        for level in reversed(range(self.max_level)):
            while (next_block := current.forward_links[level]) < item:
                current = next_block
            path[level] = current

        removed = path[0].forward_links[0]
        if removed != item:
            raise KeyError(item)

        # Update pointers and skips.
        for level in range(removed.max_level):
            previous = path[level]
            previous.forward_links[level] = removed.forward_links[level]
            previous.skips[level] += removed.skips[level] - 1

        # More skips.
        for level in range(removed.max_level, self.max_level):
            path[level].skips[level] -= 1

        self._len -= 1

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def __iter__(self):
        current = self._head.forward_links[0]
        while current is not TAIL:
            yield current.value
            current = current.forward_links[0]

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}], p={self.p})'

    def _str_helper(self, level):
        SPACING = 5

        yield f'HEAD{"-" * (SPACING + 2) * (self._head.skips[level] - 1)}->'

        current = self._head.forward_links[level]
        while current is not TAIL:
            yield f'{repr(current.value)[:SPACING]:^{SPACING}}{"-" * (SPACING + 2) * (current.skips[level] - 1)}->'
            current = current.forward_links[level]

        yield f'TAIL'

    def __str__(self):
        return '\n'.join(''.join(self._str_helper(level)) for level in reversed(range(self.max_level)))
