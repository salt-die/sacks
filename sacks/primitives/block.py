class Block:
    """Primitive element of a doubly-linked list.
    """
    __slots__ = 'val', 'prev', 'next', 'list', 'is_removed',

    def __init__(self, val=None, prev=None, next=None, list=None):
        self.val = val
        self.prev = prev or self
        self.next = next or self

        self.list = list
        self.is_removed = True

        self.insert()

    # `remove` and `insert` together implement "dancing links" [https://en.wikipedia.org/wiki/Dancing_Links]
    # Our blocks are responsible for keeping the length of the list updated. List methods will typically
    # only remove blocks at either end, but some structures might keep a mapping of these blocks so that
    # middle ones can be removed.  In this case, it's easier to pass the responsibility of updating the
    # length of the list to the blocks themselves.
    def remove(self):
        """Remove this block from its list (by linking its neighbors).
        """
        if self.is_removed:
            return

        self.prev.next = self.next
        self.next.prev = self.prev

        self.is_removed = True
        self.list._len -= 1

    def insert(self):
        """Insert this block into its list.
        """
        if not self.is_removed:
            return

        self.prev.next = self.next.prev = self

        self.is_removed = False
        self.list._len += 1

    def pop(self):
        """Remove this block from its list, de-reference its links, and return its `val`.
        """
        self.remove()

        # Remove possible circular references keeping this object alive
        self.next = self.prev = None

        return self.val
