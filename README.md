# Sacks

An odd collection of odd collections!

* heaps
    * FibonacciHeap - A priority queue consisting of heap-ordered trees.
    * MeldableHeap - A heap-ordered binary tree with O(ln n) worst-case performance with small constant factors.
    * PairingHeap - A simple heap-ordered tree with excellent practical performance.
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
* sequences
    * Column - A immutable view of the `i`th entry of each sequence in a sequence of sequences.
    * IndexedSet - An indexable set.
    * Necklace - An immutable sequence that "wraps-around".
    * Rope - A binary-tree that allows efficient manipulation of variable-length types.
    * SkipList - An ordered sequence with O(log n) search and insertion.
    * SortedList - Another ordered sequence using Python's built-in types. (A slim version of https://github.com/grantjenks/python-sortedcontainers/.)
    * View - A mutable view of a sequence.
* sets
    * AVLTree - A self-balancing binary search tree.
    * BinarySearchTree - A binary tree with O(log n) containment, addition and deletion of items.
    * BloomFilter - A memory-efficient data structure with probabalistic membership checks.  (requires `bitarray`)
    * DisjointSetForest (or UnionFind) - A collection of disjoint sets with very fast `union` and `find` operations.
    * OrderedSet - An ordered set.
    * RefinementPartition - A collection of disjoint subsets with very fast refinement.  The dual of UnionFind.
    * Setch - Set with choice. Exposes a sequence of the items of the set, `as_sequence`, for use with `random` module.
