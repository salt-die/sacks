# Sacks

An odd collection of odd collections!

* heaps
    * FibonacciHeap - A priority queue consisting of heap-ordered trees.
    * MeldableHeap - A heap-ordered binary tree with O(ln n) worst-case performance with small constant factors.
* iterables
    * DoublyLinkedList - A doubly-linked list implementation for use with higher-order collections.
    * TwoStackQueue - A queue implemented with two stacks.
* iterators
    * Peek - An iterator-wrapper that allows one to peek at the next items without consuming them.
    * RingBuffer - A FIFO buffer with a fixed size.
* mappings
    * AdaptiveRadixTree - A memory-efficient trie in which each node that is the only child is merged with its parent.
    * Bijection - A one-to-one mapping. `reverse` method allows reverse-lookup.
    * Dictch - Dict with choice. Exposes a sequence of the keys of the mapping, `as_sequence`, for use with `random` module.
* primitives
    * BinaryNode - Primitive of a binary tree.
    * Block - Element of a doubly-linked list.
    * FibHeapNode - Primitive of a Fibonacci heap.  A combination of a tree node and `Block`.
    * RadixNode - A node of an adaptive radix tree.
    * RopeInternal, RopeLeaf - Nodes of a Rope.
    * SkipListBlock - Singly-linked block of a skip list.
* sequences
    * IndexedSet - An indexable set.
    * Necklace - An immutable sequence that "wraps-around".
    * Rope - A binary-tree that allows efficient manipulation of variable-length types.
    * SkipList - An ordered (and indexable) sequence with O(log n) search and insertion.
    * View - A mutable view of a sequence.
* sets
    * BloomFilter - A memory-efficient data structure with probabalistic membership checks.  (requires `bitarray`)
    * DisjointSetForest (or UnionFind) - A collection of disjoint sets with very fast `union` and `find` operations.
    * OrderedSet - An ordered set.
    * Setch - Set with choice. Exposes a sequence of the items of the set, `as_sequence`, for use with `random` module.
