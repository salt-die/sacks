from bisect import bisect_left

from .node import Node
from .sentinel import sentinel

NOT_KEY = sentinel(name='NotKey', repr='NOT_KEY')


class RadixNode(Node):
    """Primitive of an Adaptive Radix Tree.
    """
    __slots__ = 'data',

    NOT_KEY = NOT_KEY

    def __init__(self, value='', data=NOT_KEY):
        super().__init__(value)
        self.data = data

    @property
    def is_key(self):
        return self.data is not NOT_KEY

    def iter_nodes(self):
        yield self
        for child in self.children:
            yield from child.iter_nodes()

    def iter_keys(self):
        if self.is_key:
            yield self.value
        for child in self.children:
            yield from (self.value + key for key in child.iter_keys())

    def find(self, node):
        """If node is a descendent return its data, else raise a KeyError.
        """
        if not node.value:
            if self.is_key:
                return self.data
            raise KeyError(node.value)

        children = self.children

        i = bisect_left(children, node)
        if i == len(children) or children[i].matchlen(node) != len(children[i].value):
            raise KeyError(node.value)

        child = children[i]
        node.value = node.value[len(child.value):]
        return child.find(node)

    def add(self, node):
        """
        Add `node` to children.  Splits a child if necessary.

        Notes
        -----
        To track tree size we return True if the node is a new key.
        """
        if not node.value:
            is_new_key = not self.is_key
            self.data = node.data
            return is_new_key

        children = self.children

        i = bisect_left(children, node)
        if i == len(children) or not (m := children[i].matchlen(node)):
            children.insert(i, node)
            return True

        child = children[i]
        node.value = node.value[m:]
        if m < len(child.value):
            child.split(m)
        return child.add(node)

    def split(self, n):
        """
        Split this node's value at index `n` and create a new child node
        with the suffix that adopts this node's children.
        """
        self.value, suffix = self.value[:n], self.value[n:]

        new_node = RadixNode(suffix, data=self.data)
        new_node.children = self.children

        self.children = [new_node]
        self.data = NOT_KEY

    def delete(self, node):
        """Remove `node` from children.  Re-joins leafs if possible.  Raises KeyError if node isn't a descendent.
        """
        # This is organized slightly differently than `find` and `add` methods
        # as nodes have to be deleted "from the top", i.e., by their parents.
        # This because a node has no reference to its parent and can't remove itself from the parent's
        # children.

        children = self.children

        i = bisect_left(children, node)
        if i == len(children) or children[i].matchlen(node) != len(children[i].value):
            raise KeyError(node.value)

        child = children[i]
        if len(node.value) == len(child.value):
            if not child.is_key:
                raise KeyError(node.value)

            if child.children:
                child.data = NOT_KEY
                child.join()
            else:
                self.children.pop(i)
                self.join()
        else:
            node.value = node.value[len(child.value):]
            child.delete(node)

    def join(self):
        """Merge child (if only one) and if this node isn't a key.
        """
        if len(self.children) != 1 or self.is_key:
            return

        child ,= self.children
        self.value += child.value
        self.data = child.data
        self.children = child.children

    def matchlen(self, other):
        """Number of matching items at the beginning of self and other's values.
        """
        matched = 0
        for k, p in zip(other.value, self.value):
            if k != p:
                break
            matched += 1

        return matched

    def __lt__(self, other):
        """Nodes ordered by first item of value.  This is enough as values can't overlap at any given depth.
        """
        return self.value[:1] < other.value[:1]

    def __repr__(self):
        return f"{type(self).__name__}(value='{self.value}', data={self.data!r})"
