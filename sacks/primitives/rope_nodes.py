#######################################################################################
# We've set up some machinery to simplify our Rope data structure:                    #
#     * When left or right child of a RopeInternal node is set, the node will set     #
#       itself as parent to that child.                                               #
#     * When a RopeNode's parent is set it will add its weight to its parent's weight #
#       (subtracting its weight from its old parent).                                 #
#     * When a RopeNode's weight is changed it will dispatch that change to its       #
#       parent.                                                                       #
#                                                                                     #
# `EMPTY` is a sentinel node.  Child nodes assigned to falsy values will be converted #
# to `EMPTY`.                                                                         #
#######################################################################################
from abc import abstractmethod, ABC

from ._sentinel import sentinel_node
from ._tree_printer import tree_printer


class RopeNode(ABC):
    """
    The base primitive of a Rope.

    A Rope is a binary-tree that allows efficient manipulation of variable-length types.
    """
    __slots__ = '_parent', '_weight',

    def __init__(self):
        self._parent = EMPTY
        self._weight = 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent.weight -= self.weight
        self._parent = node
        node.weight += self.weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._parent.weight += value - self._weight
        self._weight = value

    @abstractmethod
    def __iter__(self):
        yield from ()

    @abstractmethod
    def iter_nodes(self):
        yield from ()

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def query(self, i):
        """
        Return the node that contains index `i` and the index of that node's sequence
        that corresponds to `i`.
        """
        pass


EMPTY = sentinel_node(
    name='RopeSentinel',
    repr='EMPTY',
    abc=RopeNode,
    methods={ 'copy': lambda self: self, 'parent': property(lambda self: self) },
    attrs={ 'weight': 0, 'height': 0 },
)


class Child:
    """
    Child node of RopeInternal.

    This property will automatically set internal node as parent to its child.
    """
    __slots__ = 'name',

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, node):
        getattr(instance, self.name, EMPTY).parent = EMPTY

        node = node or EMPTY  # None or other falsy sentinels converted to EMPTY
        # Scrub references to this node:
        if node.parent._left is node:
            node.parent._left = EMPTY
        elif node.parent._right is node:
            node.parent._right = EMPTY

        setattr(instance, self.name, node)
        node.parent = instance


class RopeInternal(RopeNode):
    """Internal node of a Rope.
    """
    __slots__ = '_left', '_right',

    left = Child()
    right = Child()

    def __init__(self, left=EMPTY, right=EMPTY):
        super().__init__()

        self.left = left
        self.right = right

    @property
    def balance_factor(self):
        return self.left.height - self.right.height  # TODO: Keep this updated as tree is mutated

    def collapse(self):
        """Trim all empty leaves from the tree.
        """
        if isinstance(self.left, RopeInternal):
            self.left.collapse()

        if isinstance(self.right, RopeInternal):
            self.right.collapse()

        if self.parent is EMPTY:  # Special case for root.
            return

        if self.left is EMPTY:
            only_child = self.right
        elif self.right is EMPTY:
            only_child = self.left
        else:
            return

        if self.parent.left is self:
            self.parent.left = only_child
        else:
            self.parent.right = only_child

    @property
    def height(self):
        return max(self.left.height, self.right.height) + 1

    def iter_nodes(self):
        yield self
        yield from self.left.iter_nodes()
        yield from self.right.iter_nodes()

    def __iter__(self):
        yield from self.left
        yield from self.right

    def copy(self):
        return type(self)(self.left.copy(), self.right.copy())

    def query(self, i):
        if i >= self.left.weight:
            return self.right.query(i - self.left.weight)

        return self.left.query(i)

    def __repr__(self):
        return f'{type(self).__name__}(left={self.left!r}, right={self.right!r})'

    def __str__(self):
        """
        Tree structure of nodes as a string.

        Notes
        -----
        Left nodes are printed above right nodes so that one can read the nodes in
        order from top to bottom.
        """
        return '\n'.join(tree_printer(str(self.weight), (self.left, self.right)))


class RopeLeaf(RopeNode):
    """Leaf node of a Rope.
    """
    __slots__ = '_sequence',

    def __init__(self, sequence=''):
        super().__init__()
        self.sequence = sequence

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, seq):
        self._sequence = seq
        self.weight = len(seq)

    @property
    def height(self):
        return 0

    def iter_nodes(self):
        yield self

    def __iter__(self):
        yield self.sequence

    def copy(self):
        return type(self)(self.sequence)

    def query(self, i):
        return self, i

    def __repr__(self):
        return f'{type(self).__name__}(sequence={self.sequence!r})'

    def __str__(self):
        return f'{self.weight} - {self.sequence!r}'
