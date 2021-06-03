from .node import BinaryNode
from .sentinel import sentinel


class BSTNode(BinaryNode):
    __slots__ = ()

    def __init__(self, key):
        self.key = key
        self.left = self.right = EMPTY

    def __contains__(self, key):
        if key < self.key:
            return key in self.left

        if key > self.key:
            return key in self.right

        return True

    def __iter__(self):
        yield from self.left
        yield self.key
        yield from self.right

    def __reversed__(self):
        yield from reversed(self.right)
        yield self.key
        yield from reversed(self.left)

    def add_key(self, key):
        if key < self.key:
            self.left = self.left.add_key(key, self)
        else:
            self.right = self.right.add_key(key, self)

        return self

    def remove_key(self, key):
        if key < self.key:
            self.left = self.left.remove_key(key)
        elif key > self.key:
            self.right = self.right.remove_key(key)
        else:
            if not self.left:
                return self.right

            if not self.right:
                return self.left

            # Replace node with its successor.
            successor = self.right
            while successor.left:
                successor = successor.left

            self.key = successor.key
            self.right = self.right.remove_key(successor.key)

        return self


def default_iter(self):
    return
    yield

def remove_key(self, key):
    raise KeyError(key)

EMPTY = sentinel(name='BSTEmptyNode', repr='EMPTY', methods={
    '__contains__': lambda self, key: False,
    '__iter__': default_iter,
    '__reversed__': default_iter,
    'add_key': BSTNode,
    'remove_key': remove_key,
})