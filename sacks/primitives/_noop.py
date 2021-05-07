
def noop(name='', default=None, repr='NOOP', **kwargs):
    """
    Build and return an instance of a "noop" class. Modifying attributes of
    this class does nothing and `__getattr__`  returns `default`. Use
    `kwargs` to set default values for specific attribtues.

    What's the point?  In tree-like structures, some nodes may have some
    children set to `None`. In this case, node methods will always have to
    check if a child is None beforehand. Alternatively, one can just set a
    node to an instance of this class:  Now methods that attempt to mutate
    the node just do nothing and methods that access its attributes get
    default values provided in `kwargs` or `default`.
    """
    kwargs |= { 'default': default, 'repr': repr }

    def __init__(self):
        for name, val in kwargs.items():
            object.__setattr__(self, name, val)

    def __setattr__(self, name, value):
        pass

    def __getattr__(self, name):
        return self.default

    def __iter__(self):
        return
        yield

    def copy(self):
        return self

    def __bool__(self):
        return False

    def __repr__(self):
        return self.repr

    methods = {
        '__slots__': tuple(kwargs),
        '__init__': __init__,
        '__setattr__': __setattr__,
        '__getattr__': __getattr__,
        '__iter__': __iter__,
        'iter_nodes': __iter__,
        'copy': copy,
        '__bool__': __bool__,
        '__repr__': __repr__,
    }

    return type(name, (), methods)()
