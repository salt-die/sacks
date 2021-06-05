from ._tree_printer import tree_printer


class BaseNode:
    """Base for a primitive element of a tree.
    """
    def __init__(self, key):
        self.key = key
        self.parent = None

    def __lt__(self, other):
        return self.key < other.key

    def __repr__(self):
        return f'{type(self).__name__}(key={self.key!r})'


class Node(BaseNode):
    def __init__(self, key):
        super().__init__(key)
        self.children = [ ]

    def __str__(self):
        return '\n'.join(tree_printer(self.key, self.children))


class SlotNode(Node):
    __slots__ = 'key', 'parent', 'children',


class BinaryNode(BaseNode):
    __slots__ = 'key', 'parent', 'left', 'right',

    def __init__(self, key):
        super().__init__(key)
        self.left = self.right = None

    @property
    def children(self):
        if self.left:
            yield self.left
        if self.right:
            yield self.right

    def __str__(self):
        return '\n'.join(tree_printer(self.key, list(self.children)))
