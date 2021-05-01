class Block:
    """Primitive element of a doubly-linked list.
    """
    __slots__ = 'val', '_prev', '_next'

    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev or self
        self.next = next or self

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, block):
        self._prev = block
        block._next = self

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, block):
        self._next = block
        block._prev = self

    def pop(self):
        """Remove this block from its list by linking its neighbors, then return its `val`.
        """
        self.prev._next = self.next
        self.next._prev = self.prev

        # Remove possible circular reference
        self._next = self._prev = None

        return self.val
