from __future__ import annotations


class Element:
    id: int
    height: float
    plateau_neighbors: set[Element]
    can_be_view_spot: bool = True

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

    def add_neighbor(self, neighbor: Element) -> None:
        """
        Handle whether an element prevents its neighbor from being a view spot by being higher or the other way round.
        Also includes handling of plateaus, if the elements are of the same height.
        """
        if neighbor.height > self.height:
            self.can_be_view_spot = False
        elif self.height > neighbor.height:
            neighbor.can_be_view_spot = False
        else:
            neighbor.add_plateau_neighbor(self)

    def add_plateau_neighbor(self, neighbor: Element) -> None:
        """
        Adds a neighboring element as a plateau neighbor, meaning it has the same height.
        Connects all neighboring elements of the same height.
        """
        for next_neighbor in self.plateau_neighbors:
            if next_neighbor.id not in (neighbor.id, self.id):
                next_neighbor.plateau_neighbors.add(neighbor)
                neighbor.plateau_neighbors.add(next_neighbor)
        self.plateau_neighbors.add(neighbor)
        neighbor.plateau_neighbors.add(self)
