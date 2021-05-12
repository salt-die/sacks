from .block import Block
from ._tree_printer import tree_printer


class FibHeapNode(Block):
    """Primitive of a Fibonacci Heap.  A combination of a tree node and a doubly-linked block.
    """
    __slots__ = 'parent', 'children', 'degree', 'marked',

    def __init__(self, value):
        super().__init__(value)

        self.parent = None
        self.children = None
        self.degree = 0
        self.marked = False

    @property
    def is_root(self):
        return self.parent is None

    def __lt__(self, other):
        return self.value < other.value

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

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'

    def __str__(self):
        return '\n'.join(tree_printer(repr(self.value), self.children or ()))
