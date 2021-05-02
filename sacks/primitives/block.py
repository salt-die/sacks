class Block:
    """Primitive element of a doubly-linked list.
    """
    __slots__ = 'val', 'prev', 'next',

    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev or self
        self.next = next or self

        self.insert()

    # remove and insert together implement "dancing links" [https://en.wikipedia.org/wiki/Dancing_Links]
    def remove(self):
        """Remove this block from its list.
        """
        self.prev.next = self.next
        self.next.prev = self.prev

    def insert(self):
        """Insert this block into its list.
        """
        self.prev.next = self.next.prev = self

    def pop(self):
        """Remove this block from its list, de-reference its links, and return its `val`.
        """
        self.remove()

        # Remove possible circular references keeping this object alive
        self.next = self.prev = None

        return self.val
