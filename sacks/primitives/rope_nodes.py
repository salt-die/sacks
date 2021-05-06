#######################################################################################
# We've set up some machinery to simplify our Rope data structure:                    #
#     * When left or right child of a RopeInternal node is set, the node will set     #
#       itself as parent to that child. ↴                                             #
#     ↳ When a RopeNode's parent is set it will add its weight to its parent's weight #
#       (subtracting its weight from its old parent). ↴                               #
#     ↳ When a RopeNode's weight is changed it will dispatch that change to its       #
#       parent.                                                                       #
#                                                                                     #
# The dummy node, `EMPTY`, lets us avoid conditionals checking nodes for existence.   #
# Operations on this node are essentially noops.                                      #
#######################################################################################
from ._noop import noop
from ._prefix import prefix

EMPTY = noop('DeadEnd', repr='EMPTY', weight=0, height=0)


class RopeNode:
    """
    The base primitive of a Rope.

    A Rope is a tree-like structure that allows efficient manipulation of variable-length types.
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

        # Remove this node from its parent.
        if self._parent._left is self:
            self._parent._left = EMPTY
        elif self._parent._right is self:
            self._parent._right = EMPTY

        node.weight += self.weight
        self._parent = node or EMPTY

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._parent.weight += value - self._weight
        self._weight = value


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
        getattr(instance, self.name).parent = EMPTY
        node = node or EMPTY
        node.parent = instance
        setattr(instance, self.name, node)


class RopeInternal(RopeNode):
    """Internal node of a Rope.
    """
    __slots__ = '_left', '_right',

    left = Child()
    right = Child()

    def __init__(self, left=None, right=None):
        super().__init__()
        self._left = self._right = EMPTY

        self.left = left
        self.right = right

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

    def __repr__(self):
        return f'{type(self).__name__}(left={self.left!r}, right={self.right!r})'

    def __str__(self):
        """Tree structure of nodes as a string.
        """
        lines = [ str(self.weight) ]

        if self.left and self.right:
            first, second = self.left, self.right
        elif self.left:
            first, second = None, self.left
        elif self.right:
            first, second = None, self.right
        else:
            first, second = None, None

        if first:
            head, *body = str(first).splitlines()
            lines.append(f'├─{head}')
            lines.extend(prefix(body,'│ '))

        if second:
            head, *body = str(second).splitlines()
            lines.append(f'╰─{head}')
            lines.extend(prefix(body,'  '))

        return '\n'.join(lines)


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

    def __repr__(self):
        return f'{type(self).__name__}(sequence={self.sequence!r})'

    def __str__(self):
        return f'{self.weight} - {self.sequence!r}'
