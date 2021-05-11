from collections.abc import Sized, Iterable
from collections import defaultdict


class DisjointSetForest(Sized, Iterable):
    """
    A collection of disjoint sets with very fast `union` and `find` operations.

    Parameters
    ----------
    n:
        Initial number of disjoint sets. (default: 0)

    Notes
    -----
    `union` and `find` operations are O(α(n)) with n sets where α(n) is the inverse Ackermann function.
    This data structure is famously used for Kruskal's algorithm for finding minimum spanning trees.
    """
    def __init__(self, n=0):
        self.parents = list(range(n))
        self.ranks = [0] * n

    @property
    def size(self):
        return len(self.parents)

    def __len__(self):
        """The number of disjoint sets.
        """
        return len(set(self.parents))

    def __iter__(self):
        """Yield each disjoint set as a list of its members.
        """
        sets = defaultdict(list)
        for i in range(self.size):
            sets[self.find(i)].append(i)
        yield from sets.values()

    def makeset(self, n=1):
        """Add `n` more disjoint sets to the forest.
        """
        self.parents.extend(range(self.size, self.size + n))
        self.ranks.extend(0 for _ in range(n))

    def find(self, i):
        """Return the representative member of set `i`.
        """
        parents = self.parents

        if i == parents[i]:
            return i

        parents[i] = self.find(parents[i])  # Path compression
        return parents[i]

    def union(self, i, j):
        """Merge sets `i` and `j`.
        """
        i_rep = self.find(i)
        j_rep = self.find(j)

        if i_rep == j_rep:  # Already unioned
            return

        ranks = self.ranks
        parents = self.parents

        if ranks[i_rep] < ranks[j_rep]:
            parents[i_rep] = j_rep
        elif ranks[j_rep] < ranks[i_rep]:
            parents[j_rep] = i_rep
        else:
            parents[i_rep] = j_rep
            ranks[j_rep] += 1

    def is_disjoint(self, i, j):
        """Return True if sets `i` and `j` are disjoint.
        """
        return self.find(i) != self.find(j)

    def __repr__(self):
        return f'{type(self).__name__}(n={self.size})'

    def __str__(self):
        as_strings = (f'({", ".join(map(str, group))})' for group in self)
        return f'{{{", ".join(as_strings)}}}'
