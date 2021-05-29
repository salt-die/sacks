from ._tree_printer import tree_printer


class BaseNode:
    """Base for a primitive element of a tree.
    """
    __slots___ = 'key', 'parent',

    def __init__(self, key):
        self.key = key
        self.parent = None

    def __lt__(self, other):
        return self.key < other.key

    def __repr__(self):
        return f'{type(self).__name__}(key={self.key})'


class Node(BaseNode):
    __slots__ = 'children',

    def __init__(self, key):
        super().__init__(key)
        self.children = [ ]

    def __str__(self):
        return '\n'.join(tree_printer(self.key, self.children))


class BinaryNode(BaseNode):
    __slots__ = 'left', 'right',

    def __init__(self, key):
        super().__init__(key)
        self.left = None
        self.right = None

    def __str__(self):
        return '\n'.join(tree_printer(self.key, (self.left, self.right)))
