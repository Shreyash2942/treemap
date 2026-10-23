# Graph Report - .  (2026-10-23)

> Token usage is unavailable in this environment. No measured input/output token cost is claimed.

## Corpus Check
- Corpus is ~7,620 words - fits in a single context window. You may not need a graph.

## Summary
- 207 nodes · 503 edges · 10 communities detected
- Extraction: 50% EXTRACTED · 50% INFERRED · 0% AMBIGUOUS · INFERRED: 253 edges (avg confidence: 0.8)
- Token cost: unavailable (not metered in this environment).

## Community Hubs (Navigation)
- [[_COMMUNITY_BST and Behavioral Tests|BST and Behavioral Tests]]
- [[_COMMUNITY_TreeMap Integration|TreeMap Integration]]
- [[_COMMUNITY_Shared Test Infrastructure|Shared Test Infrastructure]]
- [[_COMMUNITY_Balance Algorithms and Reports|Balance Algorithms and Reports]]
- [[_COMMUNITY_Storage and Traversal Contracts|Storage and Traversal Contracts]]
- [[_COMMUNITY_Architecture and Design Rationale|Architecture and Design Rationale]]
- [[_COMMUNITY_Node Types and Module Imports|Node Types and Module Imports]]
- [[_COMMUNITY_Planned ListMap Baseline|Planned ListMap Baseline]]
- [[_COMMUNITY_Planned ASCII Rendering|Planned ASCII Rendering]]
- [[_COMMUNITY_Planned Visualization Package|Planned Visualization Package]]

## God Nodes (most connected - your core abstractions)
1. `BinarySearchTree` - 40 edges
2. `TreeNode` - 35 edges
3. `assert_bst_valid()` - 31 edges
4. `TreeMap` - 23 edges
5. `analyze_balance()` - 16 edges
6. `main()` - 12 edges
7. `test_fifty_entries_support_key_types_and_heterogeneous_values()` - 10 edges
8. `test_deep_map_integrates_sorted_traversal_balance_and_deletion()` - 10 edges
9. `Implemented BinarySearchTree core` - 10 edges
10. `test_mixed_map_operations_match_dictionary()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Generic TreeNode with comparable keys and unrestricted values` --documents--> `TreeNode`  [EXTRACTED]
  docs/architecture.md → src\bst_map\core\node.py
- `Immutable BalanceReport: edge height, root factor, unbalanced keys, overall balance` --documents--> `BalanceReport`  [EXTRACTED]
  docs/architecture.md → src\bst_map\core\balance.py
- `Implemented iterative balance analysis of every subtree` --documents--> `analyze_balance()`  [EXTRACTED]
  docs/architecture.md → src\bst_map\core\balance.py
- `Iterative height and balance analysis; reports imbalance without rotations.  Hei` --uses--> `TreeNode`  [INFERRED]
  src\bst_map\core\balance.py → src\bst_map\core\node.py
- `Tree height, root balance factor, and unbalanced keys in post-order.` --uses--> `TreeNode`  [INFERRED]
  src\bst_map\core\balance.py → src\bst_map\core\node.py

## Communities

### Community 0 - "BST and Behavioral Tests"
Cohesion: 0.11
Nodes (38): BinarySearchTree, Store key-value pairs in strict BST order without automatic balancing.      Keys, Insert a key or replace its value; an update does not change size., Return the matching node, or `None` if key is absent.          Returning a node, Remove key and return its old value; raise `KeyError` if absent.          Two-ch, Return the smallest-key node; raise `ValueError` on an empty tree., Return the largest-key node; raise `ValueError` on an empty tree., assert_bst_valid() (+30 more)

### Community 1 - "TreeMap Integration"
Cohesion: 0.15
Nodes (25): bst_map.maps.tree_map module reference, main(), Ordered maps backed by the project's data structures., TreeMap contract and integration with BST traversal, deletion, and balance., test_collections_are_sorted_by_keys_and_return_independent_lists(), test_deep_map_integrates_sorted_traversal_balance_and_deletion(), test_default_is_returned_unchanged_only_for_missing_keys(), test_empty_map_contract() (+17 more)

### Community 2 - "Shared Test Infrastructure"
Cohesion: 0.08
Nodes (21): bst_map module reference, bst_map.core module reference, bst_map.maps module reference, collections module reference, conftest module reference, Shared fixtures and an independent, iterative BST invariant validator., Return the seven-node example from the README., sample_tree() (+13 more)

### Community 3 - "Balance Algorithms and Reports"
Cohesion: 0.13
Nodes (21): analyze_balance(), balance_factor(), BalanceReport, height(), is_balanced(), Iterative height and balance analysis; reports imbalance without rotations.  Hei, Tree height, root balance factor, and unbalanced keys in post-order., Inspect all subtrees in one O(n) pass without mutation or recursion.      Pendin (+13 more)

### Community 4 - "Storage and Traversal Contracts"
Cohesion: 0.11
Nodes (21): BalanceReport.is_balanced property, Return whether every node's absolute balance factor is at most 1., BinarySearchTree.root property, Return the root for inspection, or `None` for an empty tree., Return the number of distinct keys in O(1) time., collections.abc module reference, Implemented lazy in-order, pre-order, and post-order node iterators, A key-value entry with optional children; nodes compare by identity.      Values (+13 more)

### Community 5 - "Architecture and Design Rationale"
Cohesion: 0.12
Nodes (22): A zero root balance factor does not guarantee balanced descendants, Implemented iterative balance analysis of every subtree, Planned repeatable TreeMap versus ListMap search benchmarks, Implemented BinarySearchTree core, bstkit modular educational BST toolkit, Support for trees deeper than Python's recursion limit, Graphify architecture snapshot; token usage unavailable; not a correctness proof, Strict bounds, dictionary workloads, and independent breadth-first height checks (+14 more)

### Community 6 - "Node Types and Module Imports"
Cohesion: 0.11
Nodes (13): bst_map.core.balance module reference, bst_map.core.bst module reference, bst_map.core.node module reference, bst_map.core.operations module reference, bst_map.core.traversals module reference, Iterative, unbalanced binary search tree with unique comparable keys., Comparable, Keys must support `<` and equality with a consistent total ordering.      All ke (+5 more)

### Community 7 - "Planned ListMap Baseline"
Cohesion: 1.0
Nodes (1): Reserved for the list-backed benchmark baseline.

### Community 8 - "Planned ASCII Rendering"
Cohesion: 1.0
Nodes (1): Reserved for ASCII tree rendering in a later milestone.

### Community 9 - "Planned Visualization Package"
Cohesion: 1.0
Nodes (1): Tree visualization planned for a later milestone.

## Knowledge Gaps
- **30 isolated node(s):** `Run the Day 1 and Day 2 examples with `python examples/demo.py`.`, `Educational binary search tree and map toolkit.`, `Generic nodes and the key-ordering contract shared by the BST modules.`, `Keys must support `<` and equality with a consistent total ordering.      All ke`, `Return whether this key precedes another key.` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Planned ListMap Baseline`** (2 nodes): `Reserved for the list-backed benchmark baseline.`, `list_map.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Planned ASCII Rendering`** (2 nodes): `tree_renderer.py`, `Reserved for ASCII tree rendering in a later milestone.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Planned Visualization Package`** (2 nodes): `__init__.py`, `Tree visualization planned for a later milestone.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BinarySearchTree` connect `BST and Behavioral Tests` to `TreeMap Integration`, `Shared Test Infrastructure`, `Balance Algorithms and Reports`, `Storage and Traversal Contracts`, `Architecture and Design Rationale`, `Node Types and Module Imports`?**
  _High betweenness centrality (0.302) - this node is a cross-community bridge._
- **Why does `TreeNode` connect `Storage and Traversal Contracts` to `BST and Behavioral Tests`, `Shared Test Infrastructure`, `Balance Algorithms and Reports`, `Architecture and Design Rationale`, `Node Types and Module Imports`?**
  _High betweenness centrality (0.232) - this node is a cross-community bridge._
- **Why does `TreeMap` connect `TreeMap Integration` to `BST and Behavioral Tests`, `Architecture and Design Rationale`, `Node Types and Module Imports`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `BinarySearchTree` (e.g. with `TreeNode` and `Binary search tree nodes, operations, and analysis.`) actually correct?**
  _`BinarySearchTree` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `TreeNode` (e.g. with `BalanceReport` and `Iterative height and balance analysis; reports imbalance without rotations.  Hei`) actually correct?**
  _`TreeNode` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `assert_bst_valid()` (e.g. with `test_height_root_factor_and_all_unbalanced_nodes()` and `test_analysis_does_not_change_nodes_or_rotate_tree()`) actually correct?**
  _`assert_bst_valid()` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `TreeMap` (e.g. with `BinarySearchTree` and `Ordered maps backed by the project's data structures.`) actually correct?**
  _`TreeMap` has 11 INFERRED edges - model-reasoned connections that need verification._

## Extraction Audit Notes

- Snapshot covers implemented Day 2 code and all three project documents. Generated artifacts and caches are excluded via `.graphifyignore`.
- All extracted edges have numeric confidence 1.0. Existing inferred scores were retained; 43 syntactic identifier-use edges without scores received 0.8 as direct static evidence. Scores are heuristic judgments, not calibrated probabilities.
- Added 18 imported-module reference nodes from actual Python import statements and resolved two documented property nodes from class definitions. Four package docstring nodes with colliding extractor IDs were namespaced by source file, avoiding a false shared hub.
- Static name resolution can merge similarly named methods and cannot prove runtime call targets. Inferred links should be checked against source before relying on them.
- Token accounting is unavailable. Internal extraction-schema zero counters are placeholders; `cost.json` uses null values and an explicit availability flag.
- Graph retrieval context-size estimates are separate from the project search-performance benchmarks. No TreeMap-versus-ListMap speed comparison has been run.

## Graph Retrieval Estimate

See `retrieval_benchmark.json` for reproducible context-size estimates on project questions. These are not measured language-model token consumption or BST timings.
