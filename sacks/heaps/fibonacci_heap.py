from ..primitives import FibHeapNode

INF = float('inf')

def merge_lists(a, b):
    """Merge two linked lists and return the least node.
    """
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
    current = trees

    while True:
        try:
            other = degree_table.pop(current.degree)
        except KeyError:
            degree_table[current.degree] = current

            if (current := current.next) is trees:
                break
        else:
            current, child = sorted((other, current))
            current.add_child(child)

    return min(trees)


class Entry:
    """An interface for decreasing/deleting a key in a Fibonacci heap. Tree nodes will stay private.
    """
    __slots__ = '_node', '_heap'
    def __init__(self, node, heap):
        self._node = node
        self._heap = heap

    @property
    def value(self):
        return self._node.val

    def decrease_key(self, value):
        if value >= self.value:
            raise ValueError(f'{value} greater than {self.value}')

        self._heap.decrease_key(self._node, value)

    def delete(self):
        self._heap.delete(self._node)


class FibonacciHeap:
    def __init__(self):
        self.min_root = None
        self._size = 0

    def __len__(self):
        return self._size

    def heappush(self, value):
        node = FibHeapNode(value)
        self.min_root = merge_lists(self.min_root, node)
        self._size += 1
        return Entry(node, self)

    def heappop(self):
        if not self:
            raise IndexError('pop from empty heap')

        self._size -= 1

        roots = self.min_root.next

        try:
            return self.min_root.pop()

        finally:
            if self._size == 0:
                self.min_root = None

            else:
                children = self.min_root.children

                for root in children:
                    root.parent = None

                self.min_root = merge_trees(merge_lists(self.min_root, children))

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

        self.min_root = merge_lists(self.min_root, node)

    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.heappop()
