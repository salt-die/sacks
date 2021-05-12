from .block import Block
from ._sentinel import sentinel

EMPTY = sentinel('NoNode', repr='EMPTY', methods={ 'link': lambda self, other: other })


class FibHeapNode(Block):
    """Primitive of a Fibonacci Heap.  A combination of a tree node and a doubly-linked block.
    """
    __slots__ = 'parent', 'children', 'degree', 'marked',

    def __init__(self, value):
        super().__init__(value)

        self.parent = None
        self.children = EMPTY
        self.degree = 0
        self.marked = False

    @property
    def is_root(self):
        return bool(self.parent)

    def __lt__(self, other):
        return self.value < other.value

    def add_child(self, child):
        child.parent = self
        self.degree += 1
        self.children.link_before(child)

    def link_before(self, other):
        """Link before other.
        """
        other.remove()
        other.next = self.next
        other.prev = self
        other.insert()

    def __iter__(self):
        yield current := self
        while (current := current.next) is not self:
            yield current
