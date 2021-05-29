from .block import Block
from .node import Node


class FibHeapNode(Block, Node):
    """Primitive of a Fibonacci Heap.  A combination of a tree node and a doubly-linked block.
    """
    __slots__ = 'key', 'parent', 'children', 'degree', 'marked',

    def __init__(self, key):
        super().__init__()
        self.key = key
        self.parent = None
        self.children = None
        self.degree = 0
        self.marked = False

    @property
    def is_root(self):
        return self.parent is None

    def add_child(self, child):
        child.remove()
        child.parent = self
        self.degree += 1

        if self.children:
            child.next = self.children
            child.prev = self.children.prev
            child.insert()
        else:
            self.children = child
            child.prev = child.next = child

    def __iter__(self):
        yield (current := self)
        while (current := current.next) is not self:
            yield current
