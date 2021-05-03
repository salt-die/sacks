from bisect import bisect

def prefix(body, prefix):
    """Yields each line of `body` prefixed with `prefix`. Helper for `RadixNode`'s `__str__` method.
    """
    for line in body:
        yield prefix + line

NO_DATA = object()


class RadixNode:
    """
    Primitive of an Adaptive Radix Tree.

    Notes
    -----
    `prefix`s should be sequences that are comparable with `<`.  Typical use-case is for strings (as in auto-complete).
    """
    __slots__ = 'prefix', 'data', 'children',

    def __init__(self, prefix='', data=NO_DATA):
        self.prefix = prefix
        self.data = data
        self.children = [ ]

    def add(self, node):
        """Add `node` to children.  Splits a child if necessary.
        """
        if not node.prefix:
            self.data = node.data
            return

        children = self.children

        i = bisect(children , node)
        if i < len(children) and (m := children[i].matchlen(node)):
            child = children[i]
        elif 0 < i and (m := children[i - 1].matchlen(node)):
            child = children[i - 1]
        else:
            return children.insert(i, node)

        node.prefix = node.prefix[m:]
        if m < len(child.prefix):
            child.split(m)
        child.add(node)

    def split(self, n):
        """
        Split this node's prefix at index `n`.  Creating a new child node with the suffix
        that adopts this node's children.
        """
        self.prefix, suffix = self.prefix[:n], self.prefix[n:]
        new_node = RadixNode(suffix, data=self.data)
        new_node.children = self.children
        self.children = [new_node]
        self.data = NO_DATA

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
        lines = [self.prefix or 'root']
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
