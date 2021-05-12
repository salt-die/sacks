from abc import ABC, abstractmethod
from collections.abc import Sized


class Heap(ABC, Sized):
    @abstractmethod
    def heappop(self):
        """Pop the smallest item off the heap, maintaining the heap invariant.
        """
        pass

    @abstractmethod
    def heappush(self, value):
        """Push item onto heap, maintaining the heap invariant.
        """
        pass