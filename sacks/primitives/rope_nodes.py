#######################################################################################
# Setting up some machinery to simplify our Rope data structure:                      #
#     * We use a dummy node, `EMPTY`, so we don't have to check nodes for existence.  #
#     * When left or right child of a RopeInternal node is set, the node will set     #
#       itself as parent to that child.                                               #
#     * When a RopeNode's parent is set it will add its weight to its parent's weight #
#       (subtracting its weight from its old parent).                                 #
#     * When a RopeNode's weight is changed it will dispatch that change to its       #
#       parent.                                                                       #
#######################################################################################

EMPTY = type('EMPTY', (), {
    '__repr__': lambda self: 'EMPTY',
    'weight': property(lambda self: 0, lambda self, val: None),  # weight will always be 0
    'height': 0,
})()


class RopeNode:
    """Base Node
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
        self._parent.weight += self.weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._parent.weight += value - self.weight
        self._weight = value


class Child:
    """Child node properties for rope internal nodes.
    """
    __slots__ = 'name'

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __set__(self, instance, node):
        getattr(instance, self.name).parent = EMPTY

        node = node or EMPTY
        setattr(instance, self.name, node)
        node.parent = instance

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


class RopeInternal(RopeNode):
    """Internal node of a Rope
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


class RopeLeaf(RopeNode):
    """Leaf node of a Rope
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
