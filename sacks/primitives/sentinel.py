from abc import ABCMeta
from inspect import isgeneratorfunction, signature

def sentinel(name='', default=None, repr='SENTINEL', abc=None, methods=None, attrs=None):
    """
    Build a better sentinel!
        * Modifying attributes of this object does nothing (with no errors).
        * Abstract methods in `abc` (an abstract base class) not provided in `methods` will return `default`.
        * If a value in `methods` is `"identity"` a property that returns the sentinel will be provided.
        * If a value in `methods` is `"default_iter"` a default iterator will be provided.
        * If a value in `methods` is a subclass of `Exception` a default function that raises will be provided.

    Parameters
    ----------
    name: str
        The type name. (default: '')

    default: Any
        Return value for un-implemented abstract methods and `__getattr__`. (default: None)

    repr: str
        `__repr__` string.  (default: 'SENTINEL')

    abc (optional): ABCMeta
        An abstract base class for this object. Abstract methods will be given a default implementation.

    methods (optional): dict
        Additional methods for this object.

    attrs (optional): dict
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
    Instead we can create a sentinel that *does* implement Node:
    ```
    EMPTY = sentinel(methods={ 'iter_nodes': 'default_iter' })
    ```

    And now our method can be re-written:
    ```
        def iter_nodes(self):
            yield self
            yield from self.left.iter_nodes()
            yield from self.right.iter_nodes()
    ```

    A nicer, simpler implementation!
    """
    attrs = attrs or { }
    methods = methods or { }

    @property
    def identity(self):
        return self

    def default_iter(self):
        return
        yield

    def error_factory(error):
        def error_raiser(self, *args):
            raise error(*args)

        return error_raiser

    for key, value in methods.items():
        if value == 'identity':
            methods[key] = identity
        elif value == 'default_iter':
            methods[key] = default_iter
        elif isinstance(value, type) and issubclass(value, Exception):
            methods[key] = error_factory(value)

    def __init__(self):
        for attr, val in attrs.items():
            object.__setattr__(self, attr, val)

    namespace = {
        '__slots__': tuple(attrs),
        '__init__': __init__,
        '__setattr__': lambda self, attr, value: None,
        '__getattr__': lambda self, attr: default,
        '__bool__': lambda self: False,
        '__repr__': lambda self: repr,
    }

    if abc:
        METHOD_TEMPLATE = f'def {{}}{{}}:\n    return {default}\n    {{}}\n'
        for method_name in abc.__abstractmethods__:
            method = getattr(abc, method_name)
            source = METHOD_TEMPLATE.format(method_name, signature(method), 'yield' if isgeneratorfunction(method) else '')
            exec(source, globals(), namespace)

        namespace |= methods
        return ABCMeta(name, (abc, ), namespace)()

    namespace |= methods
    return type(name, (), namespace)()
