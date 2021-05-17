class SkipListBlock:
    """Primitive of a Skip List.  Each block is singly-linked to several other blocks.
    """
    __slots__ = 'value', 'forward_links', 'skips',

    def __init__(self, value, forward_links, skips):
        self.value = value
        self.forward_links = forward_links
        self.skips = skips

    @property
    def max_level(self):
        return len(self.forward_links)

    def __le__(self, other):
        return self.value <= other.value

    def __repr__(self):
        return f'{type(self).__name__}(value={self.value})'
