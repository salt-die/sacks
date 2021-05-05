#######################################################################################
# We've set up some machinery to simplify our Rope data structure:                    #
#     * When left or right child of a RopeInternal node is set, the node will set     #
#       itself as parent to that child. ↴                                             #
#     ↳ When a RopeNode's parent is set it will add its weight to its parent's weight #
#       (subtracting its weight from its old parent). ↴                               #
#     ↳ When a RopeNode's weight is changed it will dispatch that change to its       #
#       parent.                                                                       #
#######################################################################################
from ._prefix import prefix


class RopeNode:
    """
    The base primitive of a Rope.

    A Rope is a tree-like structure that allows efficient manipulation of variable-length types.
    """

    __slots__ = '_parent', '_weight',

    def __init__(self):
        self._parent = None
        self._weight = 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if self._parent is not None:
            # Remove this node from its parent.
            if self._parent._left is self:
                self._parent._left = None
            elif self._parent._right is self:
                self._parent._right = None

            self._parent.weight -= self.weight

        if node is not None:
            node.weight += self.weight

        self._parent = node

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if self._parent is not None:
            self._parent.weight += value - self._weight

        self._weight = value


class RopeInternal(RopeNode):
    """Internal node of a Rope.
    """

    __slots__ = '_left', '_right',

    def __init__(self, left=None, right=None):
        super().__init__()
        self._left = self._right = None

        self.left = left
        self.right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        if self._left is not None:
            self._left.parent = None

        if node is not None:
            node.parent = self

        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        if self._right is not None:
            self._right.parent = None

        if node is not None:
            node.parent = self

        self._right = node

    @property
    def height(self):
        return max(self.left.height if self.left else 0, self.right.height if self.right else 0) + 1

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

    def __repr__(self):
        return f'{type(self).__name__}(sequence={self.sequence!r})'

    def __str__(self):
        return f'{self.weight} - {self.sequence!r}'
