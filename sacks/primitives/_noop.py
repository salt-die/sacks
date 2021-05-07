from abc import ABCMeta
from inspect import isgeneratorfunction, signature

def noop(name='', _default=None, _repr='NOOP', abc=None, methods=None, **attrs):
    """
    Build and return a "noop" object. Modifying attributes of this object
    does nothing (are noops!). Methods in `abc` not provided in `methods` will
    return `_default`.  Attributes not in `attrs` will return `_default`.

    Parameters
    ----------
    name: str
        The type name. (default: '')

    _default: Any
        Return value for abstract methods and value for missing `attrs`. (default: None)

    _repr: str
        `__repr__` string.  (default: 'NOOP')

    abc (optional): ABCMeta
        An abstract base class for this object.

    methods (optional): dict
        Additional methods for this object.

    **attrs (optional):
        Additional default values for this object.

    Notes
    -----
    What's the point? Say we have a simple Node class:

    ```
    class Node:
        def __init__(self, left=None, right=None):
            self.left = left
            self.right = right
    ```

    Where we set empty nodes to `None`. Our nodes might have a method to iterate through the tree:
    ```
        def iter_nodes(self):
            yield self
            if self.left is not None:
                yield from self.left.iter_nodes()
            if self.right is not None:
                yield from self.right.iter_nodes()
    ```

    The issue is that `None` doesn't implement `Node` so we need to special-case it in all our methods.
    Instead we can create an object that *does* implement Node:
    ```
    def iter_nodes(self):
        return
        yield

    EMPTY = noop(methods={ 'iter_nodes': iter_nodes })
    ```

    And now our class can be re-written:
    ```
    class Node:
        def __init__(self, left=EMPTY, right=EMPTY):
            self.left = left
            self.right = right

        def iter_nodes(self):
            yield self
            yield from self.left.iter_nodes()
            yield from self.right.iter_nodes()
    ```

    A nicer implementation!
    """

    def __init__(self):
        for attr, val in attrs.items():
            object.__setattr__(self, attr, val)

    def __setattr__(self, name, value):
        pass

    def __getattr__(self, name):
        return _default

    def __bool__(self):
        return False

    def __repr__(self):
        return _repr

    namespace = {
        '__slots__': tuple(attrs),
        '__init__': __init__,
        '__setattr__': __setattr__,
        '__getattr__': __getattr__,
        '__bool__': __bool__,
        '__repr__': __repr__,
    }

    if abc:
        METHOD_TEMPLATE = f'def {{}}{{}}:\n    return {_default}\n    {{}}\n'
        for method_name in abc.__abstractmethods__:
            method = getattr(abc, method_name)
            source = METHOD_TEMPLATE.format(method_name, signature(method), 'yield' if isgeneratorfunction(method) else '')
            exec(source, globals(), namespace)

        namespace |= methods
        return ABCMeta(name, (abc, ), namespace)()

    namespace |= methods
    return type(name, (), namespace)()
