from typing import Any

from mesh.element import Element


def find_view_spots(json_data: dict[str, Any], amount: int) -> list[Element]:
    """
    Parse the elements from the given json data and find the best <amount> view spots.
    """
    elements = _parse_elements(json_data)
    _calculate_possible_view_spots(elements, json_data)
    return _find_required_view_spots(elements, amount)


def _parse_elements(json_data: dict[str, Any]) -> dict[int, Element]:
    return {element['element_id']: Element(element['element_id'], element['value']) for element in json_data['values']}


def _calculate_possible_view_spots(elements: dict[int, Element], json_data: dict[str, Any]) -> None:
    """
    Iterate over all elements and all their nodes to find neighbors and determine whether an element could be a view
    spot.
    This uses the Element.add_neighbor() method which changes the element objects given in <elements>.
    """
    nodes: dict[int, list[int]] = dict()
    for _element in json_data['elements']:
        element = elements[_element['id']]
        for node_id in _element['nodes']:
            neighbor_ids = nodes.setdefault(node_id, list())
            for neighbor_id in neighbor_ids:
                element.add_neighbor(elements[neighbor_id])
            neighbor_ids.append(element.id)


def _find_required_view_spots(elements: dict[int, Element], amount: int) -> list[Element]:
    """
    Sort elements and find the first <amount> elements that can be a view spot.
    This also handles plateaus (neighboring elements of the same height) and only assumes the first of those
    can be view spots.

    :param elements: the existing and parsed elements
    :param amount: the (maximum) amount of view spots to find
    :return: a list of the first <amount> view spots
    """
    used_for_plateau: set[int] = set()
    result = list()
    for element in sorted(elements.values(), key=lambda e: e.height, reverse=True):
        if element.can_be_view_spot and element.id not in used_for_plateau:
            result.append(element)
            # early return if enough view spots have been found already
            if len(result) >= amount:
                return result
            # make all plateau neighbors be unavailable for use as a view spot
            used_for_plateau.update([neighbor.id for neighbor in element.plateau_neighbors])
    return result
