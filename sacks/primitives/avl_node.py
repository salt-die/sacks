from .bst_node import BSTNode
from .sentinel import sentinel


class AVLNode(BSTNode):
    __slots__ = '_left', '_right', 'balance'

    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = self.right = EMPTY
        self.balance = 0

    @property
    def is_left_child(self):
        return self.parent and self.parent.left is self

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node
        node.parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        node.parent = self

    def add_key(self, key, parent=None):
        if key < self.key:
            self.left, unbalanced_node = self.left.add_key(key, self)
        else:
            self.right, unbalanced_node = self.right.add_key(key, self)

        return self, unbalanced_node

    def remove_key(self, key):
        if key < self.key:
            self.left, unbalanced_node = self.left.remove_key(key)
        elif key > self.key:
            self.right, unbalanced_node = self.right.remove_key(key)
        else:
            if not self.left:
                return self.right, self.parent

            if not self.right:
                return self.left, self.parent

            # Replace node with its successor.
            successor = self.right
            while successor.left:
                successor = successor.left

            self.key = successor.key
            self.right, unbalanced_node = self.right.remove_key(successor.key)

        return self, unbalanced_node


def default_iter(self):
    return
    yield

def remove_key(self, key):
    raise KeyError(key)

EMPTY = sentinel(
    name='AVLEmptyNode',
    repr='EMPTY',
    methods={
        '__contains__': lambda self, key: False,
        'add_key': lambda self, key, parent=None: (AVLNode(key, parent), parent),
        'remove_key': remove_key,
        '__iter__': default_iter,
        '__reversed__': default_iter,
        'left': property(lambda self: self),
        'right': property(lambda self: self),
    },
    attrs={'balance': 0},
)
