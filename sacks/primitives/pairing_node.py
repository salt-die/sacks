from ._tree_printer import tree_printer


class PairingNode:
    """Primitive of a PairingHeap.
    """
    __slots__ = 'value', 'children',

    def __init__(self, value, children=None):
        self.value = value
        self.children = children or [ ]

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f'{type(self).__name__}(value={self.value}, children={self.children!r})'

    def __str__(self):
        return '\n'.join(tree_printer(repr(self.value), self.children))
