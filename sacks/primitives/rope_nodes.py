#######################################################################################
# We've set up some machinery to simplify our Rope data structure:                    #
#     * When left or right child of a RopeInternal node is set, the node will set     #
#       itself as parent to that child. ↴                                             #
#     ↳ When a RopeNode's parent is set it will add its weight to its parent's weight #
#       (subtracting its weight from its old parent). ↴                               #
#     ↳ When a RopeNode's weight is changed it will dispatch that change to its       #
#       parent.                                                                       #
#                                                                                     #
# `EMPTY` is a special node for empty nodes. This node is only used internally;       #
# Externally, assigning children or parents to None is still fine as setters will     #
# convert None to EMPTY.                                                              #
#######################################################################################
from abc import abstractmethod, ABC

from ._noop import noop
from ._prefix import prefix


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

        # Remove this node from its old parent.
        if self._parent._left is self:
            self._parent._left = EMPTY
        elif self._parent._right is self:
            self._parent._right = EMPTY

        self._parent = node or EMPTY
        self._parent.weight += self.weight

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


EMPTY = noop(name='RopeDeadEnd', _repr='EMPTY', abc=RopeNode, methods={ 'copy': lambda self: self }, weight=0, height=0)


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

        setattr(instance, self.name, node or EMPTY)
        getattr(instance, self.name).parent = instance


class RopeInternal(RopeNode):
    """Internal node of a Rope.
    """
    __slots__ = '_left', '_right',

    left = Child()
    right = Child()

    def __init__(self, left=None, right=None):
        super().__init__()

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

    def copy(self):
        return type(self)(self.left.copy(), self.right.copy())

    def __repr__(self):
        return f'{type(self).__name__}(left={self.left!r}, right={self.right!r})'

    def __str__(self):
        """
        Tree structure of nodes as a string.

        Note left nodes are printed above right nodes so that one can read the nodes in order from top to bottom.
        """
        lines = [ str(self.weight) ]

        head, *body = str(self.left).splitlines()
        lines.append(f'├─{head}')
        lines.extend(prefix(body,'│ '))

        head, *body = str(self.right).splitlines()
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

    def copy(self):
        return type(self)(self.sequence)

    def __repr__(self):
        return f'{type(self).__name__}(sequence={self.sequence!r})'

    def __str__(self):
        return f'{self.weight} - {self.sequence!r}'
