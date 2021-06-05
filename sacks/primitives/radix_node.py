from .node import Node
from .sentinel import sentinel
from ..sets import AVLTree

NOT_KEY = sentinel(name='NotKey', repr='NOT_KEY')


def successor(key, bst):
    """Return the least key greater or equal to `key[:1]` in the binary search tree `bst` or None.
    """
    key = key[:1]
    least_greatest, current = None, bst.root

    while current:
        if key == current.key.key:
            return current.key

        if key < current.key.key:
            least_greatest, current = current.key, current.left
        else:
            current = current.right

    return least_greatest


class RadixNode(Node):
    """Primitive of an Adaptive Radix Tree.
    """
    __slots__ = 'key', 'parent', 'children', 'value',

    def __init__(self, key='', value=NOT_KEY, parent=None):
        self.key = key
        self.parent = parent
        self.children = AVLTree()
        self.value = value

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

        if (succ := successor(key, self.children)) and (n := len(succ)) == succ.matchlen(key):
            return succ.find( key[n:] )

        raise KeyError(key)

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

        if not (succ := successor(key, self.children)) or (n := succ.matchlen(key)) == 0:
            self.children.add( RadixNode(key, value, self) )
            return True

        if n < len(succ):
            succ.split(n)

        return succ.add(key[n:], value)

    def split(self, n):
        """
        Split this node's key at index `n` and create a new child node
        with the suffix. The new node adopts this node's children.
        """
        new_node = RadixNode(self.key[n:], self.value, self)
        self.children, new_node.children = new_node.children, self.children

        for child in new_node.children:
            child.parent = new_node

        self.children.add(new_node)
        self.key = self.key[:n]
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

        if (succ := successor(key, self.children)) and (n := len(succ)) == succ.matchlen(key):
            return succ.delete( key[n:] )

        raise KeyError(key)

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
        return self.key[:1] < other.key[:1]

    def __repr__(self):
        return f'{type(self).__name__}(key={self.key!r}, value={self.value!r})'
