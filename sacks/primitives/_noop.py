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

    Where we set empty nodes to None. Our Nodes might have a method to iterate through the tree:
    ```
        def iter_nodes(self):
            yield self
            if self.left:
                yield from self.left.iter_nodes()
            if self.right:
                yield from self.right.iter_nodes()
    ```

    Alternatively, we could set empty nodes to the object returned by this function (with appropriate
    arguments) and our method becomes:
    ```
        def iter_nodes(self):
            yield self
            yield from self.left.iter_nodes()
            yield from self.right.iter_nodes()
    ```

    We can eliminate nearly all conditionals in our Node class this way.  (e.g., we've just
    shortcutted a way to create a DeadEndNode instance that "implements" the Node api.)
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
        METHOD_TEMPLATE = (
            'def {}{}:\n'
            f'    return {_default}\n'
            '    {}\n'
        )
        for method_name in abc.__abstractmethods__:
            method = getattr(abc, method_name)
            source = METHOD_TEMPLATE.format(method_name, signature(method), 'yield' if isgeneratorfunction(method) else '')
            exec(source, globals(), namespace)

        namespace |= methods
        return ABCMeta(name, (abc, ), namespace)()

    namespace |= methods
    return type(name, (), namespace)()
