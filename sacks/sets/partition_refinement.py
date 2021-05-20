from collections.abc import Iterable, Sized
from collections import defaultdict


class PartitionRefinement(Iterable, Sized):
    """A collection of disjoint subsets with very fast refinement.
    """
    def __init__(self, iterable=()):
        S = set(iterable)
        self._sets = { id(S): S }
        self._partition = dict.fromkeys(S, S)

    @property
    def size(self):
        """Number of members of all subsets.
        """
        return len(self._partition)

    def __len__(self):
        """Number of disjount subsets.
        """
        return len(self._sets)

    def __getitem__(self, item):
        """Return set that contains `item`.
        """
        return self._partition[item]

    def __iter__(self):
        yield from self._sets.values()

    def add(self, item, S):
        """Add `item` to subset `S`.
        """
        S.add(item)
        self._partition[item] = S

    def remove(self, item):
        """Remove item from partition.
        """
        self._partition.pop(item).remove(item)

    def refine(self, S):
        """Refine each set, A, in the partition into A & S and A - S. Return a list of pairs (A & S, A - S).
        """
        intersections = defaultdict(set)
        for item in S:
            if item in self._partition:
                intersections[ id(self._partition[item]) ].add(item)

        refined_sets = [ ]
        for A, AS in intersections.items():
            A = self._sets[A]
            if AS != A:
                self._sets[id(AS)] = AS
                for item in AS:
                    self._partition[item] = AS
                A -= AS
                refined_sets.append((A, AS))
        return refined_sets

    def __repr__(self):
        return f'{{{", ".join(repr(subset) for subset in self)}}}'
