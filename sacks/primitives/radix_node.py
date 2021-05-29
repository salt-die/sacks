from bisect import bisect_left

from .node import Node
from .sentinel import sentinel

NOT_KEY = sentinel(name='NotKey', repr='NOT_KEY')


class RadixNode(Node):
    """Primitive of an Adaptive Radix Tree.
    """
    __slots__ = 'value',

    def __init__(self, key='', value=NOT_KEY, parent=None):
        super().__init__(key)
        self.value = value
        self.parent = parent

    def __len__(self):
        return len(self.key)

    @property
    def is_key(self):
        return self.value is not NOT_KEY

    def iter_nodes(self):
        yield self

        for child in self.children:
            yield from child.iter_nodes()

    def iter_keys(self):
        if self.is_key:
            yield self.key

        for child in self.children:
            yield from (self.key + key for key in child.iter_keys())

    def iter_values(self):
        if self.is_key:
            yield self.value

        for child in self.children:
            yield from child.iter_values()

    def iter_items(self):
        if self.is_key:
            yield self.key, self.value

        for child in self.children:
            yield from ((self.key + key, value) for key, value in child.iter_items())

    def matchlen(self, other):
        """Return length of common prefix.
        """
        matched = 0
        for k, p in zip(self.key, other):
            if k != p:
                break
            matched += 1

        return matched

    def find(self, key):
        """Return value associated with key.
        """
        if not key:
            if self.is_key:
                return self.value
            raise KeyError(key)

        children = self.children

        i = bisect_left(children, key)
        if i == len(children) or len(child := children[i]) != child.matchlen(key):
            raise KeyError(key)

        return child.find(key[len(child):])

    def add(self, key, value):
        """
        Add `key` to children.  Splits a child if necessary.

        Notes
        -----
        To track tree size we return True if the node is a new key.

        """
        if not key:
            try:
                return not self.is_key
            finally:
                self.value = value

        children = self.children

        i = bisect_left(children, key)
        if i == len(children) or (n := children[i].matchlen(key)) == 0:
            children.insert(i, RadixNode(key, value, self))
            return True

        child = children[i]
        if n < len(child):
            child.split(n)

        return child.add(key[n:], value)

    def split(self, n):
        """
        Split this node's key at index `n` and create a new child node
        with the suffix. The new node adopts this node's children.
        """
        new_node = RadixNode(self.key[n:], self.value, self)
        new_node.children = self.children
        for child in new_node.children:
            child.parent = new_node

        self.key = self.key[:n]
        self.children = [ new_node ]
        self.value = NOT_KEY

    def delete(self, key):
        """Remove key from children.  Re-joins leafs if possible.
        """
        if not key:
            if not self.is_key:
                raise KeyError(key)

            self.value = NOT_KEY

            if self.children:
                self.join()
            elif self.parent is not None:
                self.parent.children.remove(self)
                self.parent.join()
            return

        children = self.children
        i = bisect_left(children, key)
        if i == len(children) or len(child := children[i]) != child.matchlen(key):
            raise KeyError(key)

        child.delete(key[len(child):])

    def join(self):
        """Re-join lonely children to their parent.
        """
        if len(self.children) != 1 or self.is_key or self.parent is None:
            return

        child, = self.children

        self.key += child.key
        self.value = child.value
        self.children = child.children

        for child in self.children:
            child.parent = self

    def __lt__(self, other):
        return self and other and self.key[0] < other[0]

    def __repr__(self):
        return f'{type(self).__name__}(key={self.key!r}, value={self.value!r})'
