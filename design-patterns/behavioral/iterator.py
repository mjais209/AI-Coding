"""Iterator: access elements of a collection sequentially without exposing its underlying representation."""

from collections.abc import Iterator


class TreeNode:
    def __init__(self, value: int, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.value, self.left, self.right = value, left, right


class InOrderIterator(Iterator[int]):
    def __init__(self, root: TreeNode | None) -> None:
        self._stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: TreeNode | None) -> None:
        while node:
            self._stack.append(node)
            node = node.left

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        self._push_left(node.right)
        return node.value


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, value: int) -> None:
        if self.root is None:
            self.root = TreeNode(value)
            return
        node = self.root
        while True:
            side = "left" if value < node.value else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, TreeNode(value))
                return
            node = child

    def __iter__(self) -> InOrderIterator:
        return InOrderIterator(self.root)


def main() -> None:
    tree = BinarySearchTree()
    for v in (50, 30, 70, 20, 40, 60, 80):
        tree.insert(v)
    print(f"In-order traversal: {list(tree)}")


if __name__ == "__main__":
    main()
