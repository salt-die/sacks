def prefix(body, prefix):
    """Yields each line of `body` prefixed with `prefix`. Useful for printing trees.
    """
    for line in body:
        yield prefix + line
