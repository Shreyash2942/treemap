"""Run the Day 1 BST example with `python examples/demo.py` after installation."""

from bst_map import BinarySearchTree


def main() -> None:
    tree = BinarySearchTree[int, str]()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key, f"value-{key}")

    found = tree.search(40)
    print(f"Search 40: {found.value if found is not None else 'missing'}")
    print(f"Minimum key: {tree.minimum().key}")
    print(f"Maximum key: {tree.maximum().key}")
    print(f"Delete 30: {tree.delete(30)}")
    print(f"Remaining entries: {len(tree)}")


if __name__ == "__main__":
    main()
