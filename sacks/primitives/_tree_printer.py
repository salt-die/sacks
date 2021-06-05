def snake(head, tail, text):
    """
    Helper function for `tree_printer`.

    Yields first line of text prefixed with `head`, and the remaining lines prefixed with 'tail'.
    """
    first, *rest = text.splitlines()
    yield head + first
    yield from (tail + line for line in rest)

def tree_printer(root, children):
    """Pretty prints a tree.
    """
    yield repr(root)

    if not children:
        return

    *children, last = children
    for child in children:
        yield from snake('├─', '│ ', str(child))
    yield from snake('╰─', '  ', str(last))
