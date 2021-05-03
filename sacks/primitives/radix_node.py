from bisect import bisect

def prefix(body, prefix):
    """Yields each line of `body` prefixed with `prefix`. Helper for `RadixNode`'s `__str__` method.
    """
    for line in body:
        yield prefix + line

NOT_A_KEY = type('NOT_A_KEY', (), {'__repr__': lambda self: 'NOT_A_KEY'})()  # Sentinel / Indicates a node is not a key of the tree, but just a passing node.


class RadixNode:
    """Primitive of an Adaptive Radix Tree.
    """
    __slots__ = 'prefix', 'data', 'children',

    def __init__(self, prefix='', data=NOT_A_KEY):
        self.prefix = prefix
        self.data = data
        self.children = [ ]

    @property
    def is_key(self):
        return self.data is not NOT_A_KEY

    def iter_nodes(self):
        yield self
        for child in self.children:
            yield from child.iter_nodes()

    def iter_keys(self):
        if self.is_key:
            yield self.prefix
        for child in self.children:
            yield from (self.prefix + key for key in child.iter_keys())

    def find(self, node):
        """If node is a descendent return its data, else raise a KeyError.
        """
        if not node.prefix:
            if self.is_key:
                return self.data
            raise KeyError(node.prefix)

        children = self.children

        i = bisect(children, node)
        if i < len(children) and children[i].matchlen(node) == len(children[i].prefix):
            child = children[i]
        elif 0 < i and children[i - 1].matchlen(node) == len(children[i - 1].prefix):
            child = children[i - 1]
        else:
            raise KeyError(node.prefix)

        node.prefix = node.prefix[len(child.prefix):]
        return child.find(node)

    def add(self, node):
        """Add `node` to children.  Splits a child if necessary.  To track tree size we return True if the node is a new key.
        """
        if not node.prefix:
            new_key = not self.is_key
            self.data = node.data
            return new_key

        children = self.children

        i = bisect(children, node)
        if i < len(children) and (m := children[i].matchlen(node)):
            child = children[i]
        elif 0 < i and (m := children[i - 1].matchlen(node)):
            child = children[i - 1]
        else:
            children.insert(i, node)
            return True

        node.prefix = node.prefix[m:]
        if m < len(child.prefix):
            child.split(m)
        return child.add(node)

    def split(self, n):
        """
        Split this node's prefix at index `n`.  Creating a new child node with the suffix
        that adopts this node's children.
        """
        self.prefix, suffix = self.prefix[:n], self.prefix[n:]

        new_node = RadixNode(suffix, data=self.data)
        new_node.children = self.children

        self.children = [new_node]
        self.data = NOT_A_KEY

    def delete(self, node):
        """Remove `node` from children.  Re-joins leafs if possible.
        """
        # This conditional is only for the root node.
        if not node.prefix:
            if self.is_key:
                self.data = NOT_A_KEY
                return
            raise KeyError(node.prefix)

        # This is organized slightly differently than `is_descendent` and `add` methods
        # as nodes have to be deleted "from the top", i.e., by their parents.
        # This because a node has no reference to its parent and can't remove itself from the parent's
        # children.

        children = self.children

        i = bisect(children, node)
        if i < len(children) and children[i].matchlen(node) == len(children[i].prefix):
            child = children[i]
        elif 0 < i and children[i - 1].matchlen(node) == len(children[i - 1].prefix):
            i -= 1
            child = children[i]
        else:
            raise KeyError(node.prefix)

        if len(node.prefix) == len(child.prefix):
            if not child.is_key:
                raise KeyError(node.prefix)

            if child.children:
                child.data = NOT_A_KEY
                child.join()
            else:
                self.children.pop(i)
                self.join()
        else:
            node.prefix = node.prefix[len(child.prefix):]
            child.delete(node)

    def join(self):
        """
        If this node contains no data and only has a single child node,
        adopt the child node's children and data.
        """
        if len(self.children) != 1 or self.is_key:
            return

        child ,= self.children
        self.prefix += child.prefix
        self.data = child.data
        self.children = child.children

    def matchlen(self, other):
        """Number of matching characters at the beginning of self and other's prefixes.
        """
        matched = 0
        for k, p in zip(other.prefix, self.prefix):
            if k != p:
                break
            matched += 1

        return matched

    def __lt__(self, other):
        """Nodes ordered by prefix.
        """
        return self.prefix < other.prefix

    def __repr__(self):
        return f"{type(self).__name__}(prefix='{self.prefix}', data={self.data!r})"

    def __str__(self):
        """Tree structure of nodes as a string.
        """
        lines = [repr(self.prefix)]
        if self.children:
            *children, last = self.children

            for child in children:
                first, *rest = str(child).splitlines()
                lines.append(f'├─{first}')
                lines.extend(prefix(rest,'│ '))

            first, *rest = str(last).splitlines()
            lines.append(f'╰─{first}')
            lines.extend(prefix(rest,'  '))

        return '\n'.join(lines)
