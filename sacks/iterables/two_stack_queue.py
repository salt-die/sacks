from collections.abc import Collection, Reversible


class TwoStackQueue(Collection, Reversible):
    """
    A queue implemented with two stacks.

    Notes
    -----
    This has the same amortized time complexity as a linked-list queue, but individual operations can be as much as O(n).

    The use of method names `append` and `popleft` mirrors the stdlib deque. (This queue has no `appendleft` or `pop`.)

    """
    def __init__(self, iterable=()):
        self._in = [ ]
        self._out = [ ]

        self.extend(iterable)

    def __contains__(self, item):
        for element in self:
            if item == element:
                return True
        return False

    def __iter__(self):
        yield from reversed(self._out)
        yield from self._in

    def __reversed__(self):
        yield from reversed(self._in)
        yield from self._out

    def __len__(self):
        return len(self._in) + len(self._out)

    def append(self, item):
        self._in.append(item)

    def popleft(self):
        if not self._out:
            if not self._in:
                raise IndexError('pop from empty queue')

            while self._in:
                self._out.append(self._in.pop())

        return self._out.pop()

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}])'
