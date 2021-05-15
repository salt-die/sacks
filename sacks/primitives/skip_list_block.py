from ._tree_printer import tree_printer


class SkipListBlock:
    """Primitive of a Skip List.  Each block is singly-linked to several other blocks.
    """
    __slots__ = 'value', 'height', 'forwards', 'weights',

    def __init__(self, value, height):
        self.value = value
        self.height = height

        self.forwards = [ ]
        self.weights = [ ]

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f'{type(self).__name__}(value={self.value})'

    def __str__(self):
        return '\n'.join(tree_printer(repr(self), list(map(repr, self.forwards))))

