#!/usr/bin/env python
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass(eq=True, frozen=True)
class Artifact:
    """Artifact representation."""

    name: str = field()
    id_: int = field()


@dataclass
class Node:
    """Simple node for BST."""

    value: Artifact = field()
    left: Node | None = field(default=None)
    right: Node | None = field(default=None)

    def insert(self, value: Artifact) -> None:
        """Inserting a new node."""
        # print(self.value.name, end="-") # For p2
        if value.id_ < self.value.id_:
            # Insert on the left
            if not self.left:
                self.left = Node(value=value)
            else:
                self.left.insert(value=value)

        else:
            if not self.right:
                self.right = Node(value=value)
            else:
                self.right.insert(value=value)


class BST:
    """Simple Binary Search Tree."""

    def __init__(self, value: Artifact | None = None) -> None:
        self.root: Node | None = Node(value=value) if value else None

    def insert(self, value: Artifact) -> None:
        """Insert a new node into the BST."""
        if not self.root:
            self.root = Node(value=value)

        else:
            self.root.insert(value=value)

    def bfs(self) -> dict[int, list[Artifact]]:
        """Perform a Breadth First Search on the Tree, returning a dictionary of Artifacts on each level."""
        res: dict[int, list[Artifact]] = defaultdict(list)

        if self.root is None:
            return res

        q: deque[tuple[Node, int]] = deque([(self.root, 1)])

        while q:
            node, layer = q.popleft()
            res[layer].append(node.value)

            if node.left:
                q.append((node.left, layer + 1))

            if node.right:
                q.append((node.right, layer + 1))

        return res

    def dfs_to_target(self, target: int) -> list[Artifact]:
        """Perform a DFS to get the path to a certain target."""
        res: list[Artifact] = []

        if self.root is None:
            return res

        q: deque[Node] = deque([self.root])

        while q:
            node: Node = q.pop()

            # Break if target is reached
            if node.value.id_ == target:
                break

            res.append(node.value)

            if target < node.value.id_:
                if node.left is not None:
                    q.append(node.left)

            else:
                if node.right is not None:
                    q.append(node.right)

        return res


def solve() -> None:
    """Solve the problems."""
    use_example: bool = True
    file: str = "day15.em" if use_example else "day15.in"

    # Format: ozNxANO | 576690
    sections: list[str] = open(file).read().split("\n\n")

    tree: BST = BST()
    for artifact in sections[0].strip().split("\n"):
        name: str
        id_: str
        name, id_ = artifact.strip().split(" | ")
        tree.insert(value=Artifact(name=name, id_=int(id_)))

    requested_artifacts: list[Artifact] = [
        Artifact(name=name, id_=int(id_)) for name, id_ in [x.split(" | ") for x in sections[-1].strip().split("\n")]
    ]

    # Part 01
    layers: dict[int, list[Artifact]] = tree.bfs()
    artifact_layer: dict[Artifact, int] = {}

    for k, v in layers.items():
        for art in v:
            artifact_layer[art] = k

    # Getting largest layer
    largest_layer: int = max(sum(x.id_ for x in layer) for layer in layers.values())
    num_layers: int = max(layers.keys())

    p1: int = largest_layer * num_layers

    # Part 02
    # print("\n\n")
    tree.insert(value=Artifact(name="part2", id_=500000))
    p2: str = "-".join([x.name for x in tree.dfs_to_target(target=500000)])

    # Part 03
    request_01: set[Artifact] = set(tree.dfs_to_target(target=requested_artifacts[0].id_))
    request_02: set[Artifact] = set(tree.dfs_to_target(target=requested_artifacts[1].id_))
    common_ancestors: set[Artifact] = request_02 & request_01

    # Find the one that is the deepest. We can reuse the layers dict
    p3: str = ""
    lngth: int = 0

    for ca in common_ancestors:
        layer: int = artifact_layer[ca]

        if layer > lngth:
            lngth = layer
            p3 = ca.name

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
