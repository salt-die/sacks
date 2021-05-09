#######################################################################################
# We've set up some machinery to simplify our Rope data structure:                    #
#     * When left or right child of a RopeInternal node is set, the node will set     #
#       itself as parent to that child.                                               #
#     * When a RopeNode's parent is set it will add its weight to its parent's weight #
#       (subtracting its weight from its old parent).                                 #
#     * When a RopeNode's weight is changed it will dispatch that change to its       #
#       parent.                                                                       #
#                                                                                     #
# `left` or `right` nodes assigned to falsy values will be converted to `EMPTY`.      #
#######################################################################################
from abc import abstractmethod, ABC

from ._sentinel import sentinel
from ._tree_printer import tree_printer


class Strand(ABC):
    """
    A channel between a Node and its parent.

    A Strand serves three purposes:
        1) Provide a means for a child to remove its parent's reference to it.
        2) Communicate changes in weight from the child to the parent (left strands only).
        3) Provide a way for collapsing nodes to attach their child to their parent.
    """
    __slots__ = 'parent',

    def __init__(self, parent):
        self.parent = parent

    @abstractmethod
    def cut(self):
        """Remove parent's reference to a child.
        """
        ...

    @abstractmethod
    def dispatch_weight(self, delta):
        ...

    @abstractmethod
    def attach(self, child):
        ...


class LeftStrand(Strand):
    def cut(self):
        self.parent.weight -= self.parent.left.weight
        self.parent._left._strand = DANGLING
        self.parent._left = EMPTY

    def dispatch_weight(self, delta):
        self.parent.weight += delta

    def attach(self, child):
        self.parent.left = child


class RightStrand(Strand):
    def cut(self):
        self.parent.right._strand = DANGLING
        self.parent._right = EMPTY

    def dispatch_weight(self, delta):
        pass

    def attach(self, child):
        self.parent.right = child


class RopeNode(ABC):
    """
    The base primitive of a Rope.
    """
    __slots__ = '_strand', '_weight',

    def __init__(self):
        self._strand = DANGLING
        self._weight = 0

    @property
    def parent(self):
        return self._strand.parent

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand):
        self._strand.cut()
        self._strand = strand
        strand.dispatch_weight(self.weight)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._strand.dispatch_weight(value - self._weight)
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


EMPTY = sentinel(
    name='RopeSentinel',
    repr='EMPTY',
    abc=RopeNode,
    methods={ 'copy': lambda self: self },
    attrs={ '_weight': 0, 'height': 0 },
)

DANGLING = sentinel(
    name='HalfStrand',
    repr='DANGLING',
    abc=Strand,
    attrs={ 'parent': EMPTY }
)

object.__setattr__(EMPTY, '_strand', DANGLING)


class RopeInternal(RopeNode):
    """Internal node of a Rope.
    """
    __slots__ = '_left', '_right',

    def __init__(self, left=EMPTY, right=EMPTY):
        super().__init__()
        self.left = left
        self.right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        getattr(self, '_left', EMPTY).strand.cut()
        self._left = node or EMPTY
        self._left.strand = LeftStrand(self)

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        getattr(self, '_right', EMPTY).strand.cut()
        self._right = node or EMPTY
        self._right.strand = RightStrand(self)

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

        if self.strand is DANGLING:  # Special case for root.
            return

        if self.left is EMPTY:
            self.strand.attach(self.right)
        elif self.right is EMPTY:
            self.strand.attach(self.left)

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
