from random import random

from .heap import Heap
from ..primitives import BinaryNode


def meld(a, b):
    """Merge two trees into a single tree. Rough balancing achieved with a coin-flip.
    """
    if a is None:
        return b

    if b is None:
        return b

    if a > b:
        a, b = b, a

    if round(random()):
        a.left = meld(a.left, b)
    else:
        a.right = meld(a.right, b)

    return a


class MeldableHeap(Heap):
    """
    A heap-ordered binary tree with O(ln n) worst-case performance with small constant factors.

    References
    ----------
    [https://en.wikipedia.org/wiki/Randomized_meldable_heap]

    """
    def __init__(self):
        self.root = None
        self._size = 0

    def heappush(self, value):
        self.root = meld(self.root, BinaryNode(value))
        self._size += 1

    def heappop(self):
        if not self:
            raise IndexError('pop from empty heap')

        self._size -= 1

        try:
            return self.root.value

        finally:
            self.root = meld(self.root.left, self.root.right)

    def __repr__(self):
        return f'{type(self).__name__}[size={self._size}]'

    def __str__(self):
        return str(self.root)
