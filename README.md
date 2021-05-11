# Sacks

An odd collection of odd collections!

* iterables
    * DoublyLinkedList - A doubly-linked list implementation for use with higher-order collections.
* iterators
    * Peek - An iterator-wrapper that allows one to peek at the next items without consuming them.
* mappings
    * AdaptiveRadixTree - A memory-efficient trie in which each node that is the only child is merged with its parent.
    * Bijection - A one-to-one mapping. `reverse` method allows reverse-lookup.
    * Dictch - Dict with choice. Exposes a sequence of the keys of the mapping, `as_sequence`, for use with `random` module.
* primitives
    * Block - Element of a doubly-linked list.
    * RadixNode - A node of an Adaptive Radix Tree.
    * RopeInternal, RopeLeaf - Nodes of a Rope.
* sequences
    * IndexedSet - An indexable set.
    * Necklace - An immutable sequence that "wraps-around".
    * RingBuffer - A FIFO buffer with a fixed size.
    * Rope - A binary-tree that allows efficient manipulation of variable-length types.
    * View - A mutable view of a sequence.
* sets
    * BloomFilter - A memory-efficient data structure with probabalistic membership checks.  (requires `bitarray`)
    * DisjointSetForest - A collection of disjoint sets with very fast `union` and `find` operations.
    * OrderedSet - An ordered set.
    * Setch - Set with choice. Exposes a sequence of the items of the set, `as_sequence`, for use with `random` module.
