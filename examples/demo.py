"""Run the Day 1 and Day 2 examples with `python examples/demo.py`."""

from bst_map import BinarySearchTree, TreeMap
from bst_map.core import analyze_balance, inorder, postorder, preorder
from bst_map.visualization import render_tree


def main() -> None:
    tree = BinarySearchTree[int, str]()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key, f"value-{key}")

    found = tree.search(40)
    print(f"Search 40: {found.value if found is not None else 'missing'}")
    print(f"Minimum key: {tree.minimum().key}")
    print(f"Maximum key: {tree.maximum().key}")
    for traversal in [inorder, preorder, postorder]:
        print(f"{traversal.__name__}: {[node.key for node in traversal(tree.root)]}")
    report = analyze_balance(tree.root)
    print(f"Height: {report.height}; balanced: {report.is_balanced}")
    print("Before deleting 30:")
    print(render_tree(tree.root))
    print(f"Delete 30: {tree.delete(30)}")
    print("After deleting 30 (successor 40):")
    print(render_tree(tree.root))
    print(f"Remaining entries: {len(tree)}")

    skewed = BinarySearchTree[int, None]()
    for key in [1, 2, 3]:
        skewed.insert(key, None)
    print(f"Skewed tree: {analyze_balance(skewed.root)}")

    mapping = TreeMap[str, int | None]()
    mapping.put("beta", 20)
    mapping.put("alpha", 10)
    mapping.put("alpha", 15)
    mapping.put("optional", None)
    print(f"Sorted map: {mapping.items()}")
    print(f"Stored None exists: {mapping.contains_key('optional')}")
    print(f"Missing key default: {mapping.get('missing', 'fallback')}")
    print(f"Remove beta: {mapping.remove('beta')}; size: {len(mapping)}")


if __name__ == "__main__":
    main()
