from ._tree_printer import tree_printer


class BaseNode:
    """Base for a primitive element of a tree.
    """
    __slots___ = 'value', 'parent',

    def __init__(self, value):
        self.value = value
        self.parent = None

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f'{type(self).__name__}(value={self.value})'


class Node(BaseNode):
    __slots__ = 'children',

    def __init__(self, value):
        super().__init__(value)
        self.children = [ ]

    def __str__(self):
        return '\n'.join(tree_printer(self.value, self.children))


class BinaryNode(BaseNode):
    __slots__ = 'left', 'right',

    def __init__(self, value):
        super().__init__(value)
        self.left = None
        self.right = None

    def __str__(self):
        return '\n'.join(tree_printer(self.value, (self.left, self.right)))
