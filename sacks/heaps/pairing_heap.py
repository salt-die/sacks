from .heap import Heap
from ..primitives.node import SlotNode

def meld(a, b):
    """Merge two heaps, destructively.
    """
    if a is None:
        return b

    if b is None:
        return a

    if a > b:
        a, b = b, a

    a.children.append(b)
    return a

def pair(children):
    """Recursively meld a list of heaps.
    """
    if not children:
        return None

    if len(children) == 1:
        return children[0]

    first, second, *rest = children
    return meld(meld(first, second), pair(rest))


# Note if decrease_key is added to PairingHeap, SlotNode.children should be changed to a linked-list for efficient deletion operations.
class PairingHeap(Heap):
    """
    A simple heap-ordered tree with excellent practical performance.

    References
    ----------
    [https://en.wikipedia.org/wiki/Pairing_heap]

    """
    def heappush(self, key):
        self._root = meld(self._root, SlotNode(key))
        self._size += 1

    def heappop(self):
        if not self:
            raise IndexError('pop from empty heap')

        self._size -= 1

        try:
            return self._root.key
        finally:
            self._root = pair(self._root.children)

    def __repr__(self):
        return f'{type(self).__name__}[size={self._size}]'

    def __str__(self):
        return str(self._root)
