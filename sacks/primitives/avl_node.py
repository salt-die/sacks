from .bst_node import BSTNode
from .sentinel import sentinel


class AVLNode(BSTNode):
    __slots__ = '_left', '_right', 'balance',

    def __init__(self, key):
        self.key = key
        self.parent = None
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

    def add_key(self, key):
        if key < self.key:
            self.left, new_node = self.left.add_key(key)
        else:
            self.right, new_node = self.right.add_key(key)

        return self, new_node

    def remove_key(self, key):
        if key < self.key:
            self.left, unbalanced_node = self.left.remove_key(key)
        elif key > self.key:
            self.right, unbalanced_node = self.right.remove_key(key)
        else:
            if not self.left or not self.right:
                if self.parent:
                    self.parent.balance -= 1 if self.is_left_child else -1
                return self.right or self.left, self.parent

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
        'add_key': lambda self, key: (AVLNode(key), ) * 2,
        'remove_key': remove_key,
        '__iter__': default_iter,
        '__reversed__': default_iter,
        'left': property(lambda self: self),
        'right': property(lambda self: self),
    },
    attrs={
        'balance': 0,
    },
)
