from .heap import Heap, Entry
from ..primitives import FibHeapNode

def merge_lists(a, b):
    """Merge two linked lists and return the least node.
    """
    if a is None:
        return b

    if b is None:
        return a

    prev = b.prev

    b.prev = a.prev
    a.prev.next = b

    a.prev = prev
    prev.next = a

    return min(a, b)

def merge_trees(trees):
    """Merge trees in a linked list until each has a different degree.  Return the min tree.
    """
    degree_table = { }

    for root in tuple(trees):
        while True:
            if root.degree not in degree_table:
                degree_table[root.degree] = root
                break
            else:
                other = degree_table.pop(root.degree)
                root, child = sorted((root, other))
                root.add_child(child)

    return min(root)


class FibonacciHeap(Heap):
    """
    A priority queue consisting of heap-ordered trees.

    References
    ----------
    [https://en.wikipedia.org/wiki/Fibonacci_heap]

    """
    def __init__(self):
        self.root = None
        self._size = 0

    def heappush(self, value):
        node = FibHeapNode(value)
        self.root = merge_lists(self.root, node)
        self._size += 1
        return Entry(node, self)

    def heappop(self):
        if not self:
            raise IndexError('pop from empty heap')

        if self.root.next is self.root:
            roots = None
        else:
            roots = self.root.next

        result = self.root.pop()

        self._size -= 1
        if self._size == 0:
            self.root = None
        else:
            if children := self.root.children:
                for root in children:
                    root.parent = None

            self.root = merge_trees(merge_lists(roots, children))

        return result

    def decrease_key(self, node, value):
        node.value = value

        if not node.is_root and node < node.parent:
            self.cut(node)

    def cut(self, node):
        if not node.parent.is_root:
            if node.parent.marked:
                self.cut(node.parent)
            else:
                node.parent.marked = True

        node.marked = False
        node.parent = None

        self.root = merge_lists(self.root, node)

    def __repr__(self):
        return f'{type(self).__name__}[size={self._size}]'

    def __str__(self):
        return '\n'.join(map(str, self.root))
