from ._tree_printer import tree_printer


class BinaryNode:
    """Primitive of a binary tree.
    """
    __slots__ = 'value', 'left', 'right', 'parent',

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f'{type(self).__name__}(value={self.value}, left={self.left!r}, right={self.right!r})'

    def __str__(self):
        return '\n'.join(tree_printer(repr(self.value), (self.left, self.right)))
