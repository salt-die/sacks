from .heap import Heap, Entry
from ..primitives.fibonnaci_heap_node import FibHeapNode

def merge_lists(a, b):
    """Merge two linked lists and return the least node.
    """
    if a is None:
        return b

    if b is None:
        return a

    a.prev, b.prev = b.prev, a.prev

    b.prev.next = b
    a.prev.next = a

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

            child = degree_table.pop(root.degree)
            if root > child:
                root, child = child, root
            root.add_child(child)

    return min(root)


class FibonacciHeap(Heap):
    """
    A priority queue consisting of heap-ordered trees.

    References
    ----------
    [https://en.wikipedia.org/wiki/Fibonacci_heap]

    """
    def heappush(self, key):
        node = FibHeapNode(key)
        self._root = merge_lists(self._root, node)
        self._size += 1
        return Entry(node, self)

    def heappop(self):
        if not self:
            raise IndexError('pop from empty heap')

        if self._root.next is self._root:
            roots = None
        else:
            roots = self._root.next

        result = self._root.key
        self._root.pop()

        self._size -= 1
        if self._size == 0:
            self._root = None
        else:
            if children := self._root.children:
                for root in children:
                    root.parent = None

            self._root = merge_trees(merge_lists(roots, children))

        return result

    def decrease_key(self, node, key):
        node.key = key

        if node.is_root:
            self._root = min(node, self._root)
        elif node < node.parent:
            self.cut(node)

    def cut(self, node):
        if not node.parent.is_root:
            if node.parent.marked:
                self.cut(node.parent)
            else:
                node.parent.marked = True

        if node.next is node:
            node.parent.children = None
        else:
            node.parent.children = node.next

        node.marked = False
        node.parent = None
        node.remove()

        root = self._root
        node.prev, node.next = root.prev, root
        node.insert()

        self._root = min(node, root)

    def __repr__(self):
        return f'{type(self).__name__}[size={self._size}]'

    def __str__(self):
        return '\n'.join(map(str, self._root))
