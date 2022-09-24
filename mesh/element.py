from __future__ import annotations


class Element:
    id: int
    height: float
    plateau_neighbors: set[Element]
    is_view_spot: bool = True

    def __init__(self, _id: int, height: float) -> None:
        self.id = _id
        self.height = height
        self.plateau_neighbors = set()

    def __str__(self) -> str:
        return f'Element {self.id}'

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other) -> bool:
        return isinstance(other, Element) and self.id == other.id

    def add_plateau_neighbor(self, element: Element) -> None:
        for neighbor in self.plateau_neighbors:
            if neighbor.id not in (element.id, self.id):
                neighbor.plateau_neighbors.add(element)
                element.plateau_neighbors.add(neighbor)
        self.plateau_neighbors.add(element)
        element.plateau_neighbors.add(self)
